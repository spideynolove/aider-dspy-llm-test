import logging
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)

class DataValidationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Validate required fields
        required_fields = ['open', 'high', 'low', 'close', 'volume', 'timestamp']
        for field in required_fields:
            if not adapter.get(field):
                raise DropItem(f"Missing required field: {field}")
        
        # Convert numeric fields
        numeric_fields = ['open', 'high', 'low', 'close', 'volume']
        for field in numeric_fields:
            try:
                adapter[field] = float(adapter[field])
            except (ValueError, TypeError):
                raise DropItem(f"Invalid value for {field}: {adapter[field]}")
        
        return item

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            collection_name = spider.name
            self.db[collection_name].update_one(
                {'_id': item['_id']},
                {'$set': dict(item)},
                upsert=True
            )
            return item
        except Exception as e:
            logger.error(f"Error storing item in MongoDB: {e}")
            raise DropItem(f"Error storing item: {e}")
