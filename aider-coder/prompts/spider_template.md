# Scrapy Spider Template

## Description
Generate a Scrapy spider for financial data scraping. The spider should:
1. Handle pagination using base requests
2. Extract OHLCV (Open, High, Low, Close, Volume) data
3. Handle dynamic content using Scrapy-Playwright
4. Include comprehensive error handling and retry mechanisms
5. Implement rate limiting and request throttling
6. Use middleware for proxy rotation and user-agent management
7. Store data in MongoDB with custom _id generation

## Example Input
```python
{
    "website": "example.com",
    "data_type": "OHLCV",
    "pagination": "API-based",
    "dynamic_content": True,
    "storage": "MongoDB"
}
```

## Example Output
```python
import scrapy
import random
from scrapy_playwright.page import PageCoroutine

class FinancialSpider(scrapy.Spider):
    name = "financial_data"
    start_urls = ["https://example.com/api/v1/data"]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408],
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': True},
        'DOWNLOADER_MIDDLEWARES': {
            'project.middlewares.RandomUserAgentMiddleware': 543,
            'project.middlewares.ProxyMiddleware': 544,
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                'playwright': True,
                'playwright_page_coroutines': [
                    PageCoroutine('wait_for_selector', 'div.data-container', timeout=10000)
                ]
            }
        )

    def parse(self, response):
        try:
            # Extract OHLCV data
            data = {
                'open': response.css('div.open::text').get(),
                'high': response.css('div.high::text').get(),
                'low': response.css('div.low::text').get(),
                'close': response.css('div.close::text').get(),
                'volume': response.css('div.volume::text').get(),
                'timestamp': response.css('div.timestamp::text').get(),
                '_id': self.generate_id(response)
            }
            
            # Validate data before yielding
            if None in data.values():
                self.logger.warning("Missing data in item")
                return
                
            yield data

            # Handle pagination
            next_page = response.css('a.next-page::attr(href)').get()
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse,
                    meta={'playwright': True}
                )
                
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
            raise

    def generate_id(self, response):
        timestamp = response.css('div.timestamp::text').get()
        return f"{timestamp}_{self.name}"

class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

class ProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_proxy = 0

    def process_request(self, request, spider):
        if self.proxy_list:
            request.meta['proxy'] = self.proxy_list[self.current_proxy]
            self.current_proxy = (self.current_proxy + 1) % len(self.proxy_list)
