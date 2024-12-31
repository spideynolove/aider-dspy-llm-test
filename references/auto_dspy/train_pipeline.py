"""
This script loads log data, creates a DSPy dataset, and compiles the DSPy pipeline.
"""

import os
import dspy
from dotenv import load_dotenv
from dspy_pipeline.pipeline import DSPyPipeline
from dspy_pipeline.signatures import ChatCompletionSignature
from dspy_pipeline.data_loader import create_dspy_dataset_from_logs

# Load environment variables
load_dotenv('config/.env', override=True)

# Configure LLM model using environment variables
lm = dspy.LM(
    model=os.getenv('OPENAI_MODEL_ID'),
    api_key=os.getenv('OPENAI_API_KEY'),
    api_base=os.getenv('OPENAI_BASE_URL'),
    max_tokens=500,
    temperature=0.1
)

# Configure DSPy to use the LLM
dspy.configure(lm=lm)

def train_dspy_pipeline():
    """
    Loads log data, creates a DSPy dataset, and compiles the DSPy pipeline.
    """
    import os
    from pathlib import Path
    log_file_path = str(Path(__file__).parent / "api_requests.log")  # Path to your log file
    print(f"Loading log data from: {log_file_path}")
    trainset = create_dspy_dataset_from_logs(log_file_path)

    if not trainset:
        print("No training data found in log file. Skipping training.")
        return

    print(f"Training data loaded. Number of examples: {len(trainset)}")

    # Initialize and compile the DSPy pipeline
    pipeline = DSPyPipeline(student=dspy.Predict(ChatCompletionSignature))
    pipeline.compile(trainset=trainset)
    print("DSPy pipeline compiled successfully.")


if __name__ == "__main__":
    train_dspy_pipeline()
    print("Training script finished.")
    
