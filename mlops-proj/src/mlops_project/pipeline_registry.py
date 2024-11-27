"""Project pipelines."""

from typing import Dict
from kedro.pipeline import Pipeline

from .pipelines import (
    data_engineering as de,
    data_science as ds,
    model_evaluation as me,
    data_unit_tests as dt,
    data_drift as drift,
)

def register_pipelines() -> Dict[str, Pipeline]:

    data_engineering_pipeline = de.create_pipeline()
    data_science_pipeline = ds.create_pipeline()
    model_evaluation_pipeline = me.create_pipeline()
    data_unit_tests_pipeline = dt.create_pipeline()
    data_drift_pipeline = drift.create_pipeline()

    return {
        "de": data_engineering_pipeline,
        "ds": data_science_pipeline,
        "me": model_evaluation_pipeline,
        "dt": data_unit_tests_pipeline,
        "drift": data_drift_pipeline,
        "__default__": data_engineering_pipeline + data_science_pipeline + model_evaluation_pipeline
    }