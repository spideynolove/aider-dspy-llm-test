import scrapy
import json
from scrapy_playwright.page import PageCoroutine
from urllib.parse import urlencode
from sample_project.items import FinancialDataItem

class OhlcvSpider(scrapy.Spider):
    name = "ohlcv"
    allowed_domains = ["example.com"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://api.example.com/v1/ohlcv"
        self.api_key = kwargs.get('api_key')

    def start_requests(self):
        params = {
            'interval': '1d',
            'limit': 100,
            'api_key': self.api_key
        }
        url = f"{self.base_url}?{urlencode(params)}"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={
                'playwright': True,
                'playwright_page_coroutines': [
                    PageCoroutine('wait_for_selector', 'pre', timeout=10000)
                ]
            }
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            for item in data['results']:
                yield FinancialDataItem(
                    _id=item['timestamp'],
                    open=item['open'],
                    high=item['high'],
                    low=item['low'],
                    close=item['close'],
                    volume=item['volume'],
                    timestamp=item['timestamp']
                )
            
            # Handle pagination
            if data['next']:
                yield scrapy.Request(
                    url=data['next'],
                    callback=self.parse,
                    meta={'playwright': True}
                )
                
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
            yield None
