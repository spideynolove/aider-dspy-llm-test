import logging
from typing import Dict, Any
from .utils.workers import ExtractionWorker, TransformationWorker, StorageWorker

class Orchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.extraction_worker = ExtractionWorker()
        self.transformation_worker = TransformationWorker()
        self.storage_worker = StorageWorker()

    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate the scraping workflow."""
        try:
            # Step 1: Extract data
            self.logger.info("Starting extraction phase")
            raw_data = self.extraction_worker.extract(task['url'], task['extraction_rules'])
            
            # Step 2: Transform data
            self.logger.info("Starting transformation phase")
            cleaned_data = self.transformation_worker.transform(
                raw_data, 
                task['transformation_rules']
            )
            
            # Step 3: Store data
            self.logger.info("Starting storage phase")
            storage_result = self.storage_worker.store(
                cleaned_data, 
                task['storage_config']
            )
            
            # Step 4: Synthesize results
            self.logger.info("Workflow completed successfully")
            return {
                "status": "success",
                "raw_data": raw_data,
                "cleaned_data": cleaned_data,
                "storage_result": storage_result
            }
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
