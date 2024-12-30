# Sample Scrapy Project

This is a sample production-ready Scrapy project for scraping financial OHLCV data.

## Features

- **API-based scraping**: Handles API pagination and authentication
- **Data validation**: Ensures data quality before storage
- **MongoDB storage**: Stores data in MongoDB with upsert functionality
- **Playwright integration**: Handles dynamic content
- **Proxy rotation**: Implements proxy rotation for large-scale scraping
- **User-agent rotation**: Rotates user agents to avoid detection
- **Error handling**: Implements robust error handling and retry mechanisms

## Project Structure

```
sample_project/
├── scrapy.cfg
├── sample_project/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── ohlcv_spider.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy .env.example to .env and configure your settings
4. Run the spider:
   ```bash
   scrapy crawl ohlcv
   ```

## Configuration

Edit the `.env` file to configure:

- MongoDB connection settings
- API keys
- Proxy list
- User agent list
