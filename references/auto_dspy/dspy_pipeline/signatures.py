"""
This module contains signatures for various DSPy tasks.
"""

import dspy


class ChatCompletionSignature(dspy.Signature):
    """
    A signature for chat completion tasks.
    """
    question = dspy.InputField()
    answer = dspy.OutputField()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
