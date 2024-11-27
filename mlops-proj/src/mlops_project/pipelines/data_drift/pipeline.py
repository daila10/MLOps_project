"""
This is a boilerplate pipeline 'data_drift'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import  data_drift
from mlops_project.pipelines.data_engineering.nodes import clean_data, feature_engineering



def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
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
                name="feature_engineering_node",
           ),

            node(
                func= data_drift,
                inputs=["cleaned_data","drift_test",],
                outputs= "drift_result",
                name="drift_analysis",
            ),
        ]
    )
