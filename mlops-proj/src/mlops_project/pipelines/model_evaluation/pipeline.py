"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.18.8
"""
from kedro.pipeline import node, Pipeline
from .nodes import evaluate_model

def create_pipeline():
    return Pipeline(
        [
            node(
                evaluate_model,
                inputs=["y_test", "y_pred"],
                outputs=["rf_AUC_plot", "metrics"],
                name="evaluate_model_node"
            ),
        ]
    )
