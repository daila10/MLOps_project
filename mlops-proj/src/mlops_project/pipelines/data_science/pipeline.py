"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.8
"""

# Import the required functions from nodes.py
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import train_model, predict

def create_pipeline(**kwargs)-> Pipeline:
# Define the pipeline
    data_science_pipeline = Pipeline([
        node(
            train_model,
            inputs=["X_train", "y_train"],
            outputs="trained_rf",
            name="train_model_node"
        ),
        node(
            predict,
            inputs=["trained_rf", "X_test", "y_test"],
            outputs="y_pred",
            name="predict_node"
        )
    ])
    return data_science_pipeline
