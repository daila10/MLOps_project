"""
This is a boilerplate pipeline 'data_drift'
generated using Kedro 0.18.8
"""
import logging
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import shap
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import sklearn
import mlflow
import nannyml as nml

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def data_drift(data_reference: pd.DataFrame, data_analysis: pd.DataFrame):
    
    # Define the threshold for the test as parameters in the parameters catalog
    constant_threshold = nml.thresholds.ConstantThreshold(lower=0.3, upper=0.7)
    constant_threshold.thresholds(data_reference)

    # Let's initialize the object that will perform the Univariate Drift calculations
    univariate_calculator = nml.UnivariateDriftCalculator(
        column_names=["Air temperature [C]", "Process temperature [C]", "Rotational speed [rpm]",
                      "Torque [Nm]", "Tool wear [min]"],
        treat_as_categorical=[],
        chunk_size=50,
        categorical_methods=[],
        thresholds={"jensen_shannon": constant_threshold}
    )

    univariate_calculator.fit(data_reference)
    results = univariate_calculator.calculate(data_analysis).to_df()

    # Generate a report for some numeric features using KS test and Evidently AI
    data_drift_report = Report(metrics=[
        DataDriftPreset(cat_stattest='ks', stattest_threshold=0.05)]
    )

    data_drift_report.run(
        current_data=data_analysis[["Air temperature [C]", "Process temperature [C]", "Rotational speed [rpm]",
                                    "Torque [Nm]", "Tool wear [min]"]],
        reference_data=data_reference[["Air temperature [C]", "Process temperature [C]", "Rotational speed [rpm]",
                                        "Torque [Nm]", "Tool wear [min]"]],
        column_mapping=None
    )

    data_drift_report.save_html("data/07_reporting/data_drift_report.html")
    return results
