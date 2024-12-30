# Coding Conventions for Scrapy Projects

## General Guidelines

* Follow PEP 8 for Python code style
* Use consistent naming conventions (e.g., snake_case for variables and functions)
* Keep code organized and modular

## Scrapy Specific

* Use Scrapy's built-in data structures (e.g., Item, Request) instead of custom ones
* Keep spider code separate from item pipeline code
* Use Scrapy's built-in logging mechanisms instead of print statements

## Best Practices

* Test your code regularly
* Use version control (e.g., Git) to track changes
* Keep your code up-to-date with the latest Scrapy version

## Example Use Cases

* Updating Scrapy spider to use latest version of Scrapy
* Fixing Scrapy item pipeline to handle new data format
* Optimizing Scrapy project for performance

## Orchestrator-Workers Pattern

The Orchestrator-Workers pattern is used for complex scraping tasks that involve multiple steps. It divides the process into modular components:

1. **Orchestrator**: Manages the overall workflow, delegating tasks to workers and synthesizing results.
2. **Extraction Worker**: Handles data extraction from the target website.
3. **Transformation Worker**: Cleans and normalizes the extracted data.
4. **Storage Worker**: Saves the cleaned data to the database.

### Example Workflow
```python
from aider_coder.orchestrator import Orchestrator

task = {
    "url": "https://example.com",
    "extraction_rules": {...},
    "transformation_rules": {...},
    "storage_config": {...}
}

orchestrator = Orchestrator()
result = orchestrator.process(task)
```

### Benefits
- **Modularity**: Each worker focuses on a specific task.
- **Flexibility**: The orchestrator can adapt the workflow dynamically.
- **Scalability**: Workers can process data in parallel.
