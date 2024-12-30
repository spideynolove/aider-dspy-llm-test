import logging
import os
import json
from typing import Dict, Any, List
from anthropic import Anthropic

class LLMOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = os.getenv('AIDER_MODEL', 'claude-3-5-sonnet-20240620')

    def divide_tasks(self, project_description: str) -> List[Dict[str, Any]]:
        """Divide the Scrapy project into smaller tasks using the LLM."""
        prompt = f"""
        You are an AI orchestrator specializing in Scrapy projects. Break down the following project into smaller tasks:
        
        Project Description:
        {project_description}
        
        Consider these Scrapy-specific components:
        1. Spider implementation (start_urls, parsing logic)
        2. Item definition and pipeline
        3. Middleware configuration
        4. Storage backend setup
        5. Error handling and retry logic
        6. Monitoring and logging setup
        
        Return the tasks as a JSON list, where each task has:
        - "task_id": A unique ID for the task
        - "task_type": One of ["spider", "item", "middleware", "storage", "error_handling", "monitoring"]
        - "task_description": A clear description of what needs to be implemented
        - "dependencies": List of task IDs this task depends on
        - "required_files": List of files that need to be created or modified
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=1000
        )
        return json.loads(response.completion)

    def delegate_task(self, task: Dict[str, Any], project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a Scrapy-specific task to a worker LLM."""
        task_type_prompts = {
            "spider": """
                Create a Scrapy spider that:
                - Handles the website structure defined in the config
                - Implements proper parsing logic
                - Includes error handling
                - Yields structured items
            """,
            "item": """
                Define Scrapy items and pipelines that:
                - Match the required data fields
                - Implement data validation
                - Handle proper storage
            """,
            "middleware": """
                Configure Scrapy middleware that:
                - Handles rate limiting
                - Manages sessions/cookies if needed
                - Rotates user agents/proxies
            """,
            "storage": """
                Implement storage backends that:
                - Connect to specified databases
                - Handle data serialization
                - Implement proper error handling
            """,
            "error_handling": """
                Implement error handling that:
                - Catches and logs specific exceptions
                - Implements retry logic
                - Maintains error statistics
            """,
            "monitoring": """
                Set up monitoring that:
                - Tracks spider progress
                - Logs important metrics
                - Enables debugging
            """
        }

        prompt = f"""
        You are an AI worker specializing in Scrapy development. Complete the following task:
        
        Task Type: {task['task_type']}
        Task Description: {task['task_description']}
        
        Specific Requirements:
        {task_type_prompts.get(task['task_type'], '')}
        
        Project Configuration:
        {json.dumps(project_config, indent=2)}
        
        Return the result as a JSON object with:
        - "task_id": The ID of the task
        - "files": A dictionary mapping filenames to their complete content
        - "dependencies": List of Python packages required
        - "settings": Any Scrapy settings that need to be configured
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=2000
        )
        return json.loads(response.completion)

    def validate_task_result(self, task_result: Dict[str, Any]) -> bool:
        """Validate the output of a worker LLM."""
        prompt = f"""
        You are a Scrapy code validator. Validate the following task result:
        
        Task Result:
        {json.dumps(task_result, indent=2)}
        
        Check for:
        1. Proper Scrapy syntax and patterns
        2. Error handling implementation
        3. Resource cleanup
        4. Code style and documentation
        
        Return true if valid, false if not.
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=100
        )
        return response.completion.strip().lower() == "true"

    def synthesize_results(self, task_results: List[Dict[str, Any]], project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize the results from all tasks into a complete Scrapy project."""
        prompt = f"""
        You are an AI synthesizer specializing in Scrapy projects. Combine these task results into a complete project:
        
        Task Results:
        {json.dumps(task_results, indent=2)}
        
        Project Configuration:
        {json.dumps(project_config, indent=2)}
        
        Consider:
        1. Dependencies between components
        2. Configuration consistency
        3. Resource management
        4. Error handling
        5. Monitoring integration
        
        Return a JSON object with:
        - "files": Complete content for all project files
        - "settings": Final Scrapy settings
        - "requirements": Complete list of dependencies
        - "deployment": Deployment instructions
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=3000
        )
        return json.loads(response.completion)

    def process_project(self, project_description: str, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate the entire workflow for a Scrapy project."""
        try:
            # Step 1: Divide project into tasks
            self.logger.info("Dividing project into tasks")
            tasks = self.divide_tasks(project_description)
            
            # Step 2: Process tasks in dependency order
            self.logger.info("Processing tasks")
            task_results = []
            for task in tasks:
                # Check if dependencies are completed
                deps_completed = all(
                    any(r["task_id"] == dep for r in task_results)
                    for dep in task["dependencies"]
                )
                if not deps_completed:
                    continue
                
                # Delegate task to worker
                result = self.delegate_task(task, project_config)
                
                # Validate result
                if not self.validate_task_result(result):
                    raise ValueError(f"Task {task['task_id']} failed validation")
                
                task_results.append(result)
            
            # Step 3: Synthesize results
            self.logger.info("Synthesizing results")
            final_project = self.synthesize_results(task_results, project_config)
            
            self.logger.info("Project completed successfully")
            return final_project
            
        except Exception as e:
            self.logger.error(f"Project generation failed: {e}")
            raise
