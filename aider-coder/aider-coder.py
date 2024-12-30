import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from llm_orchestrator import LLMOrchestrator

class AiderCoder:
    def __init__(self, project_template: str = None):
        load_dotenv()
        self.logger = self._setup_logger()
        self.project_config = self._load_project_template(project_template)
        self.orchestrator = LLMOrchestrator()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('aider-coder')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_project_template(self, template_path: str = None) -> dict:
        if template_path is None:
            template_path = Path(__file__).parent / "project_template.json"
        
        try:
            with open(template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading project template: {e}")
            return {}

    def create_project(self, description: str) -> dict:
        """Create a new Scrapy project using the LLM orchestrator."""
        try:
            self.logger.info("Starting project creation")
            project = self.orchestrator.process_project(description, self.project_config)
            
            # Create project files
            for filename, content in project['files'].items():
                filepath = Path(filename)
                filepath.parent.mkdir(parents=True, exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write(content)
            
            self.logger.info("Project created successfully")
            return project
        except Exception as e:
            self.logger.error(f"Project creation failed: {e}")
            raise

def main():
    # Example usage
    aider = AiderCoder()
    project = aider.create_project(
        "Create a Scrapy spider to scrape financial data from example.com"
    )
    print("Project created with files:", list(project['files'].keys()))

if __name__ == "__main__":
    main()
