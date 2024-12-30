# Aider-Coder

Aider-Coder is a Python-based assistant for Scrapy project development, specifically tailored for financial data scraping. It provides tools and utilities to streamline the development and maintenance of Scrapy spiders, pipelines, and distributed crawling systems.

## Features

- **AI-Assisted Development**: Generate and optimize Scrapy spiders using Anthropic's Claude 3.5
- **Database Integration**: Built-in support for MongoDB and PostgreSQL
- **Distributed Crawling**: Utilities for Scrapy-Redis and Scrapy-Cluster
- **Dynamic Content Handling**: Integrated Scrapy-Playwright support
- **Code Validation**: Automated spider code validation
- **Configuration Management**: Centralized environment configuration
- **Orchestrator-Workers Pattern**: Modular workflow for complex scraping tasks

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aider-coder.git
   cd aider-coder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

## Usage

### Generating a Spider
```python
from aider_coder import AiderCoder

aider = AiderCoder()
spider_code = aider.generate_spider_code(
    "Scrape OHLCV data from example.com"
)
if spider_code:
    print(spider_code)
```

### Optimizing a Pipeline
```python
pipeline_code = """
# Existing pipeline code
"""
optimized_code = aider.optimize_pipeline(pipeline_code)
if optimized_code:
    print(optimized_code)
```

### Database Operations
```python
# MongoDB
collection = aider.get_mongo_collection("ohlcv_data")

# PostgreSQL
results = aider.execute_pg_query(
    "SELECT * FROM financial_data WHERE date > %s",
    ("2023-01-01",)
)
```

### Middleware Configuration
```python
# Configure default middleware
settings = aider.configure_middleware({})

# Configure proxies
proxy_settings = aider.configure_proxies([
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080'
])
```

### Testing Support
```python
# Generate test template
test_code = aider.generate_test_template("my_spider")

# Validate pipeline
is_valid = aider.validate_pipeline(pipeline_code)
```

## Configuration

Edit the `.env` file to configure:

- Anthropic API credentials
- MongoDB and PostgreSQL connection details
- Redis and Kafka settings for distributed crawling
- Scrapy-Playwright configuration

## Directory Structure

```
aider-coder/
├── .env.example            # Environment configuration template
├── aider-coder.py          # Main AiderCoder implementation
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
├── prompts/                # AI prompt templates
│   ├── spider_template.md  # Spider generation template
│   ├── pipeline_template.md# Pipeline optimization template
│   └── error_fixes.md      # Common error fixes
└── utils/                  # Utility scripts
    ├── db_utils.py         # Database utilities
    └── validation.py       # Code validation utilities
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License

MIT License
