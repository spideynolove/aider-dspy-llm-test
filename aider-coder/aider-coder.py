import os
import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from anthropic import Anthropic
from pymongo import MongoClient
import psycopg2
import redis
from scrapy.utils.project import get_project_settings

class AiderCoder:
    def __init__(self, project_template: Optional[str] = None):
        self.logger = self._setup_logger()
        self.anthropic = self._init_anthropic()
        self.mongo_client = self._init_mongo()
        self.postgres_conn = self._init_postgres()
        self.redis_client = self._init_redis()
        self.scrapy_settings = get_project_settings()
        self.project_config = self._load_project_template(project_template)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('aider-coder')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_project_template(self, template_path: Optional[str]) -> Dict[str, Any]:
        if template_path is None:
            template_path = Path(__file__).parent / "project_template.json"
        
        try:
            with open(template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading project template: {e}")
            return {}

    def _init_anthropic(self) -> Anthropic:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return Anthropic(api_key=api_key)

    def _init_mongo(self) -> MongoClient:
        mongo_uri = os.getenv('MONGO_URI')
        return MongoClient(mongo_uri)

    def _init_postgres(self):
        return psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )

    def _init_redis(self):
        return redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            db=int(os.getenv('REDIS_DB'))
        )

    def generate_spider_code(self) -> Optional[str]:
        """Generate Scrapy spider code using Anthropic API and project template"""
        try:
            prompt = self._create_spider_prompt()
            response = self.anthropic.completions.create(
                model=os.getenv('AIDER_MODEL'),
                prompt=prompt,
                max_tokens_to_sample=1000
            )
            return response.completion
        except Exception as e:
            self.logger.error(f"Error generating spider code: {e}")
            return None

    def _create_spider_prompt(self) -> str:
        """Create a prompt for spider generation based on project template"""
        template = """
        Generate a Scrapy spider for the following project:
        
        Project Name: {project_name}
        Description: {description}
        Data Type: {data_type}
        Website URL: {website_url}
        Website Structure: {website_structure}
        Output Fields: {output_fields}
        Storage: {storage}
        Settings: {settings}
        """
        
        return template.format(
            project_name=self.project_config.get('project_name', ''),
            description=self.project_config.get('description', ''),
            data_type=self.project_config.get('data_type', ''),
            website_url=self.project_config.get('website', {}).get('url', ''),
            website_structure=json.dumps(self.project_config.get('website', {}).get('structure', {}), indent=2),
            output_fields=", ".join(self.project_config.get('output', {}).get('fields', [])),
            storage=json.dumps(self.project_config.get('output', {}).get('storage', {}), indent=2),
            settings=json.dumps(self.project_config.get('settings', {}), indent=2)
        )

    def optimize_pipeline(self, pipeline_code: str) -> Optional[str]:
        """Optimize Scrapy pipeline using Anthropic API"""
        try:
            response = self.anthropic.completions.create(
                model=os.getenv('AIDER_MODEL'),
                prompt=f"Optimize this Scrapy pipeline: {pipeline_code}",
                max_tokens_to_sample=1000
            )
            return response.completion
        except Exception as e:
            self.logger.error(f"Error optimizing pipeline: {e}")
            return None

    def validate_spider(self, spider_code: str) -> bool:
        """Validate spider code structure"""
        required_methods = ['start_requests', 'parse']
        return all(method in spider_code for method in required_methods)

    def get_mongo_collection(self, collection_name: str):
        """Get MongoDB collection"""
        db = self.mongo_client[os.getenv('MONGO_DATABASE')]
        return db[collection_name]

    def execute_pg_query(self, query: str, params=None):
        """Execute PostgreSQL query"""
        with self.postgres_conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def add_to_redis_queue(self, queue_name: str, value: str):
        """Add item to Redis queue"""
        self.redis_client.rpush(queue_name, value)

    def configure_middleware(self, settings: dict) -> dict:
        """Configure common Scrapy middleware settings"""
        default_middleware = {
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            },
            'RETRY_TIMES': 3,
            'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429]
        }
        return {**default_middleware, **settings}

    def configure_proxies(self, proxy_list: list) -> dict:
        """Configure proxy settings for Scrapy"""
        return {
            'PROXY_LIST': proxy_list,
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            }
        }

    def validate_pipeline(self, pipeline_code: str) -> bool:
        """Validate pipeline code structure"""
        required_methods = ['process_item', 'open_spider', 'close_spider']
        return all(method in pipeline_code for method in required_methods)

    def generate_test_template(self, spider_name: str) -> str:
        """Generate a basic test template for a spider"""
        return f"""
import unittest
from scrapy.http import HtmlResponse
from myproject.spiders.{spider_name} import {spider_name.capitalize()}Spider

class Test{spider_name.capitalize()}Spider(unittest.TestCase):
    def setUp(self):
        self.spider = {spider_name.capitalize()}Spider()

    def test_parse(self):
        # Create a fake response
        response = HtmlResponse(
            url='http://example.com',
            body='<html></html>',
            encoding='utf-8'
        )
        
        # Test parse method
        results = list(self.spider.parse(response))
        self.assertGreater(len(results), 0)

if __name__ == '__main__':
    unittest.main()
"""

if __name__ == "__main__":
    aider = AiderCoder()
    spider_code = aider.generate_spider_code()
    if spider_code and aider.validate_spider(spider_code):
        print("Generated spider code:")
        print(spider_code)
