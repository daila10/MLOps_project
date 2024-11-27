"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from kedro.io import DataCatalog
from .nodes import clean_data, feature_engineering, split_data

def create_pipeline(**kwargs) -> Pipeline:
    """Create the Kedro pipeline."""
    pipeline = Pipeline(
        [
            node(
                clean_data,
                inputs="raw_data",
                outputs="cleaned_data",
                name="clean_data_node"
            ),
            node(
                feature_engineering,
                inputs="cleaned_data",
                outputs="engineered_data",
                name="feature_engineering_node"
            ),
            node(
                split_data,
                inputs="engineered_data",
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node"
            ),
        ]
    )
    return pipeline

