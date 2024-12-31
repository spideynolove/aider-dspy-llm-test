"""
This module contains the DSPyPipeline class, which is responsible for compiling and running DSPy pipelines.
"""

import dspy
from dspy.teleprompt import MIPROv2
from dspy_pipeline.utils import dummy_metric
from typing import List, Optional, Type

class BasePipeline:
    """Base pipeline class to provide predictor functionality"""
    def predictors(self) -> List[dspy.Predict]:
        """Returns list of predictors used in the pipeline"""
        if not hasattr(self, '_predictors'):
            self._predictors = []
        return self._predictors

class DSPyPipeline(BasePipeline):
    """
    A class to represent a DSPy pipeline, which compiles and runs DSPy pipelines using MIPROv2.
    """

    def __init__(self, metric=dummy_metric, auto="light", student=None):
        super().__init__()
        self.mipro_optimizer = MIPROv2(metric=metric, auto=auto)
        self._predictors = []  # Initialize empty predictor list
        self.predictor = None
        self.student_class = student
        if student is not None:
            # Initialize with the student predictor
            self._predictors = [dspy.Predict(student)]

    def forward(self, question: str) -> dspy.Prediction:
        """
        Executes the forward pass of the pipeline.

        Args:
            question (str): The input question to process.

        Returns:
            dspy.Prediction: The prediction result.

        Raises:
            ValueError: If the pipeline is not compiled yet.
        """
        if self.predictor is None:
            raise ValueError("Pipeline not compiled yet. Call compile() first.")
        return self.predictor(question=question)

    def compile(self, trainset: List[dspy.Example], 
                max_bootstrapped_demos: int = 3, 
                max_labeled_demos: int = 4) -> 'DSPyPipeline':
        """
        Compiles the DSPy pipeline using MIPROv2.

        Args:
            trainset (list): A list of dspy.Example objects.
            max_bootstrapped_demos (int): Maximum number of bootstrapped demos.
            max_labeled_demos (int): Maximum number of labeled demos.
            
        Returns:
            DSPyPipeline: Returns self for chaining.
        """
        if self.student_class is None:
            raise ValueError(
                "Student signature not provided. Pass a student signature to the constructor."
            )
        
        if not trainset:
            import logging
            logging.warning("No training data provided. Skipping training.")
            self.predictor = dspy.Predict(self.student_class)
            self._predictors = [self.predictor]
            return self

        # Compile using MIPROv2
        self.predictor = self.mipro_optimizer.compile(
            student=self.student_class,
            trainset=trainset,
            max_bootstrapped_demos=max_bootstrapped_demos,
            max_labeled_demos=max_labeled_demos,
            requires_permission_to_run=False,
        )
        
        # Update predictors list with compiled predictor
        self._predictors = [self.predictor]
        return self