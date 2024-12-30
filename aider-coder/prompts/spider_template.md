# Scrapy Spider Template

## Description
Generate a Scrapy spider for financial data scraping. The spider should:
1. Handle pagination using base requests
2. Extract OHLCV (Open, High, Low, Close, Volume) data
3. Handle dynamic content using Scrapy-Playwright
4. Include proper error handling and retry mechanisms
5. Store data in MongoDB with custom _id generation

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
from scrapy_playwright.page import PageCoroutine

class FinancialSpider(scrapy.Spider):
    name = "financial_data"
    start_urls = ["https://example.com/api/v1/data"]

    custom_settings = {
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                'playwright': True,
                'playwright_page_coroutines': [
                    PageCoroutine('wait_for_selector', 'div.data-container')
                ]
            }
        )

    def parse(self, response):
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
        yield data

        # Handle pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                meta={'playwright': True}
            )

    def generate_id(self, response):
        # Custom ID generation logic
        timestamp = response.css('div.timestamp::text').get()
        return f"{timestamp}_{self.name}"
