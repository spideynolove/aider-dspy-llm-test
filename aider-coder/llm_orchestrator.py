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
        """Divide the project into smaller tasks using the LLM."""
        prompt = f"""
        You are an AI orchestrator. Break down the following Scrapy project into smaller tasks:
        
        Project Description:
        {project_description}
        
        Return the tasks as a JSON list, where each task has:
        - "task_id": A unique ID for the task
        - "task_description": A clear description of the task
        - "dependencies": A list of task IDs this task depends on (if any)
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=1000
        )
        return json.loads(response.completion)

    def delegate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a task to a worker LLM."""
        prompt = f"""
        You are an AI worker. Complete the following task:
        
        Task Description:
        {task['task_description']}
        
        Return the result as a JSON object with:
        - "task_id": The ID of the task
        - "result": The completed task output
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=1000
        )
        return json.loads(response.completion)

    def synthesize_results(self, task_results: List[Dict[str, Any]]) -> str:
        """Synthesize the results from all tasks into a complete project."""
        prompt = f"""
        You are an AI synthesizer. Combine the following task results into a complete Scrapy project:
        
        Task Results:
        {json.dumps(task_results, indent=2)}
        
        Return the complete project code as a Python script.
        """
        
        response = self.anthropic.completions.create(
            model=self.model,
            prompt=prompt,
            max_tokens_to_sample=2000
        )
        return response.completion

    def process_project(self, project_description: str) -> str:
        """Orchestrate the entire workflow for a Scrapy project."""
        try:
            # Step 1: Divide tasks
            self.logger.info("Dividing project into tasks")
            tasks = self.divide_tasks(project_description)
            
            # Step 2: Delegate tasks to workers
            self.logger.info("Delegating tasks to workers")
            task_results = [self.delegate_task(task) for task in tasks]
            
            # Step 3: Synthesize results
            self.logger.info("Synthesizing results into a complete project")
            project_code = self.synthesize_results(task_results)
            
            self.logger.info("Project completed successfully")
            return project_code
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            raise
