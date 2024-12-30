import random
import logging
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)

class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_LIST', [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...'
        ])
        return cls(user_agents)

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

class ProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_proxy = 0

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.get('PROXY_LIST', [])
        return cls(proxy_list)

    def process_request(self, request, spider):
        if self.proxy_list:
            request.meta['proxy'] = self.proxy_list[self.current_proxy]
            self.current_proxy = (self.current_proxy + 1) % len(self.proxy_list)

class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status in [429]:
            retry_after = int(response.headers.get('Retry-After', 1))
            spider.logger.info(f"Rate limited. Retrying after {retry_after} seconds")
            return self._retry(request, response_status_message(response.status), spider) or response
        return super().process_response(request, response, spider)
