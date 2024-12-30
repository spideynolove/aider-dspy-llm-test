from openai import OpenAI


# Define a custom Step class if dspy.Step is not available
class Step:
    def __init__(self):
        pass

    def process(self, data):
        raise NotImplementedError(
            "Subclasses must implement the 'process' method.")


class OpenAICompatibleStep(Step):
    def __init__(self, api_key, base_url, model_id):
        super().__init__()
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_id = model_id

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
    # Replace with your actual API key
    api_key = "glhf_544c3ea34a2f1d6ea03bf6e1709cd759"
    base_url = "https://glhf.chat/api/openai/v1"
    model_id = "hf:meta-llama/Llama-3.3-70B-Instruct"

    # Create a pipeline (simplified for testing)
    def data_loader(x): return x  # Mock data loader
    openai_step = OpenAICompatibleStep(
        api_key=api_key,
        base_url=base_url,
        model_id=model_id
    )
    def model_trainer(x): return x  # Mock model trainer

    # Run the pipeline with sample data
    # sample_data = "How to start a Tech startup focused on AI?"
    sample_data = "How can i using scrapy to scrape data from a website?"
    processed_data = data_loader(sample_data)
    openai_result = openai_step.process(processed_data)
    final_result = model_trainer(openai_result)
    print("Pipeline Result:", final_result)
