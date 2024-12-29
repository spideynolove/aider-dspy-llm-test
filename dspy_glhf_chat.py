import dspy
import openai

class OpenAICompatibleStep(dspy.Step):
    def __init__(self, api_key, base_url, model_id):
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
    api_key = "glhf_544c3ea34a2f1d6ea03bf6e1709cd759"
    base_url = "https://glhf.chat/api/openai/v1"
    model_id = "hf:meta-llama/Llama-3.3-70B-Instruct"

    # Create a pipeline
    pipeline = dspy.Pipeline()
    pipeline.add_step(dspy.DataLoader())
    pipeline.add_step(OpenAICompatibleStep(
        api_key=api_key,
        base_url=base_url,
        model_id=model_id
    ))
    pipeline.add_step(dspy.ModelTrainer())

    # Run the pipeline with sample data
    sample_data = "Hello, how are you?"
    result = pipeline.run(sample_data)
    print("Pipeline Result:", result)
