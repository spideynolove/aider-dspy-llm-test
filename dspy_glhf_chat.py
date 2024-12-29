import openai

# Define a custom Step class if dspy.Step is not available
class Step:
    def __init__(self):
        pass

    def process(self, data):
        raise NotImplementedError("Subclasses must implement the 'process' method.")

class OpenAICompatibleStep(Step):
    def __init__(self, api_key, base_url, model_id):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.model_id = model_id
        openai.api_key = self.api_key
        openai.api_base = self.base_url

    def process(self, data):
        # Process data using the OpenAI-compatible API
        response = openai.Completion.create(
            model=self.model_id,
            prompt=data,
            max_tokens=100
        )
        return response.choices[0].text

# Example usage
if __name__ == "__main__":
    # Replace with your actual API key
    api_key = "your-api-key"
    base_url = "https://glhf.chat/api/openai/v1"
    model_id = "hf:meta-llama/Llama-3.3-70B-Instruct"

    # Create a pipeline (simplified for testing)
    data_loader = lambda x: x  # Mock data loader
    openai_step = OpenAICompatibleStep(
        api_key=api_key,
        base_url=base_url,
        model_id=model_id
    )
    model_trainer = lambda x: x  # Mock model trainer

    # Run the pipeline with sample data
    sample_data = "Hello, how are you?"
    processed_data = data_loader(sample_data)
    openai_result = openai_step.process(processed_data)
    final_result = model_trainer(openai_result)
    print("Pipeline Result:", final_result)
