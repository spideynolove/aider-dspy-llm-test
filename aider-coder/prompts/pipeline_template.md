# Scrapy Pipeline Template

## Description
Generate a Scrapy pipeline for processing financial data. The pipeline should:
1. Validate incoming data against specified rules
2. Clean and normalize data
3. Process items in batches for better performance
4. Store data in MongoDB with custom _id
5. Handle duplicate data and errors gracefully
6. Include comprehensive logging at different levels
7. Implement retry mechanisms for failed operations

## Example Input
```python
{
    "data_type": "OHLCV",
    "storage": "MongoDB",
    "validation_rules": {
        "required_fields": ["open", "high", "low", "close", "volume"],
        "numeric_fields": ["open", "high", "low", "close", "volume"]
    },
    "batch_size": 100
}
```

## Example Output
```python
import logging
from pymongo import MongoClient
from scrapy.exceptions import DropItem

class FinancialDataPipeline:
    def __init__(self, mongo_uri, mongo_db, batch_size=100):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.batch_size = batch_size
        self.batch = []
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            batch_size=crawler.settings.getint('BATCH_SIZE', 100)
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.logger.info(f"Connected to MongoDB at {self.mongo_uri}")

    def close_spider(self, spider):
        if self.batch:
            self.process_batch(spider)
        self.client.close()
        self.logger.info("MongoDB connection closed")

    def process_item(self, item, spider):
        try:
            # Validate and transform data
            self.validate_item(item)
            transformed_item = self.transform_item(item)
            
            # Add to batch
            self.batch.append(transformed_item)
            
            # Process batch if size reached
            if len(self.batch) >= self.batch_size:
                self.process_batch(spider)
                
            return item
            
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
            raise DropItem(f"Error processing item: {e}")

    def process_batch(self, spider):
        try:
            self.db[spider.name].insert_many(self.batch, ordered=False)
            self.logger.info(f"Successfully inserted {len(self.batch)} items")
        except Exception as e:
            self.logger.error(f"Error processing batch: {e}")
        finally:
            self.batch = []

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
        # Clean and normalize data
        return {
            'open': float(item['open']),
            'high': float(item['high']),
            'low': float(item['low']),
            'close': float(item['close']),
            'volume': int(float(item['volume'])),
            'timestamp': item['timestamp'],
            '_id': item['_id']
        }
