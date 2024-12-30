import logging
from datetime import datetime
from scrapy import signals
from scrapy.statscollectors import StatsCollector

class MonitoringExtension:
    def __init__(self, stats: StatsCollector):
        self.stats = stats
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        return ext

    def spider_opened(self, spider):
        self.logger.info(f"Spider opened: {spider.name}")
        self.stats.set_value('start_time', datetime.utcnow())

    def spider_closed(self, spider, reason):
        self.logger.info(f"Spider closed: {spider.name}, reason: {reason}")
        self.stats.set_value('end_time', datetime.utcnow())
        self._log_final_stats()

    def item_scraped(self, item, spider):
        self.stats.inc_value('item_scraped_count')
        self.stats.set_value('last_scraped_time', datetime.utcnow())

    def item_dropped(self, item, spider, exception):
        self.stats.inc_value('item_dropped_count')
        self.logger.warning(f"Item dropped: {exception}")

    def _log_final_stats(self):
        stats = self.stats.get_stats()
        self.logger.info("Final stats:")
        for key, value in stats.items():
            self.logger.info(f"{key}: {value}")
