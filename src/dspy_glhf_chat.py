from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define a custom Step class if dspy.Step is not available
class Step:
    def __init__(self):
        pass

    def process(self, data):
        raise NotImplementedError(
            "Subclasses must implement the 'process' method.")


class OpenAICompatibleStep(Step):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL')
        )
        self.model_id = os.getenv('OPENAI_MODEL_ID')

    def process(self, data):
        # Process data using the OpenAI-compatible API
        response = self.client.completions.create(
            model=self.model_id,
            prompt=data,
            max_tokens=100
        )
        return response.choices[0].text

# Example usage
if __name__ == "__main__":
    # Create a pipeline (simplified for testing)
    def data_loader(x): return x  # Mock data loader
    openai_step = OpenAICompatibleStep()
    def model_trainer(x): return x  # Mock model trainer

    # Run the pipeline with sample data
    sample_data = "How can i using scrapy to scrape data from a website?"
    processed_data = data_loader(sample_data)
    openai_result = openai_step.process(processed_data)
    final_result = model_trainer(openai_result)
    print("Pipeline Result:", final_result)
