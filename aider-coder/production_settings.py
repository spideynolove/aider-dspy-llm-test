import os
from scrapy.utils.project import get_project_settings

def get_production_settings():
    settings = get_project_settings()
    
    # Core settings
    settings.set('BOT_NAME', 'financial_data_scraper')
    settings.set('LOG_LEVEL', os.getenv('LOG_LEVEL', 'INFO'))
    settings.set('CONCURRENT_REQUESTS', int(os.getenv('CONCURRENT_REQUESTS', 8)))
    settings.set('DOWNLOAD_DELAY', float(os.getenv('DOWNLOAD_DELAY', 1.0)))
    settings.set('RETRY_TIMES', int(os.getenv('RETRY_TIMES', 3)))
    settings.set('DOWNLOAD_TIMEOUT', int(os.getenv('DOWNLOAD_TIMEOUT', 30)))
    
    # Middleware
    settings.set('DOWNLOADER_MIDDLEWARES', {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
        'scrapy_playwright.middleware.PlaywrightMiddleware': 543,
    })
    
    # Playwright settings
    settings.set('PLAYWRIGHT_BROWSER_TYPE', os.getenv('PLAYWRIGHT_BROWSER_TYPE', 'chromium'))
    settings.set('PLAYWRIGHT_LAUNCH_OPTIONS', {
        'headless': True,
        'timeout': 30000
    })
    
    # Database settings
    settings.set('MONGO_URI', os.getenv('MONGO_URI'))
    settings.set('MONGO_DATABASE', os.getenv('MONGO_DATABASE'))
    
    # Monitoring
    settings.set('STATS_CLASS', 'scrapy.statscollectors.MemoryStatsCollector')
    settings.set('EXTENSIONS', {
        'scrapy.extensions.corestats.CoreStats': 0,
        'scrapy.extensions.logstats.LogStats': 0,
        'scrapy.extensions.telnet.TelnetConsole': 0,
    })
    
    # Error tracking
    settings.set('SPIDER_MIDDLEWARES', {
        'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    })
    
    return settings
