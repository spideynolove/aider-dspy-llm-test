# Scrapy Pipeline Template

## Description
Generate a Scrapy pipeline for processing financial data. The pipeline should:
1. Validate incoming data
2. Transform data into required format
3. Store data in MongoDB with custom _id
4. Handle duplicate data
5. Include error logging and retry mechanisms

## Example Input
```python
{
    "data_type": "OHLCV",
    "storage": "MongoDB",
    "validation_rules": {
        "required_fields": ["open", "high", "low", "close", "volume"],
        "numeric_fields": ["open", "high", "low", "close", "volume"]
    }
}
```

## Example Output
```python
import logging
from pymongo import MongoClient
from scrapy.exceptions import DropItem

class FinancialDataPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = logging.getLogger(__name__)

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
            # Validate data
            self.validate_item(item)
            
            # Transform data
            transformed_item = self.transform_item(item)
            
            # Store in MongoDB
            self.db[spider.name].update_one(
                {'_id': item['_id']},
                {'$set': dict(transformed_item)},
                upsert=True
            )
            return item
            
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
            raise DropItem(f"Error processing item: {e}")

    def validate_item(self, item):
        required_fields = ['open', 'high', 'low', 'close', 'volume']
        for field in required_fields:
            if field not in item or item[field] is None:
                raise DropItem(f"Missing required field: {field}")
            
            try:
                float(item[field])
            except ValueError:
                raise DropItem(f"Invalid numeric value for field: {field}")

    def transform_item(self, item):
        return {
            'open': float(item['open']),
            'high': float(item['high']),
            'low': float(item['low']),
            'close': float(item['close']),
            'volume': int(float(item['volume'])),
            'timestamp': item['timestamp'],
            '_id': item['_id']
        }
