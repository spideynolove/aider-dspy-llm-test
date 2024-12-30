import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_NAME = 'sample_project'

SPIDER_MODULES = ['sample_project.spiders']
NEWSPIDER_MODULE = 'sample_project.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16

# Configure a delay for requests
DOWNLOAD_DELAY = 1

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'

# Middleware settings
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'sample_project.middlewares.RandomUserAgentMiddleware': 543,
    'sample_project.middlewares.ProxyMiddleware': 750,
}

# Item pipelines
ITEM_PIPELINES = {
    'sample_project.pipelines.DataValidationPipeline': 300,
    'sample_project.pipelines.MongoDBPipeline': 800,
}

# Playwright settings
PLAYWRIGHT_BROWSER_TYPE = os.getenv('PLAYWRIGHT_BROWSER_TYPE', 'chromium')
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,
    'timeout': 30000
}

# MongoDB settings
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# Retry settings
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Security settings
AUTOTHROTTLE_ENABLED = True
COOKIES_ENABLED = False
