"""
This module contains an example test.

Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.

To run the tests, run ``kedro test`` from the project root directory.
"""

from pathlib import Path

import pytest
import pandas as pd
import numpy as np

# from kedro.framework.project import settings
# from kedro.config import ConfigLoader
# from kedro.framework.context import KedroContext
# from kedro.framework.hooks import _create_hook_manager
import sys
import os

#sys.path.append("C:/Users/rosan/Desktop/class-bank-example/src/class_bank_example/pipelines/")
from mlops_project.pipelines.data_engineering.nodes import clean_data, feature_engineering

# def test_clean_data_type():
#     df = pd.read_csv("data/01_raw/predictive_maintenance.csv")
#     df_transformed, describe_to_dict, describe_to_dict_verified = clean_data(df)
#     isinstance(describe_to_dict, dict)

def test_engineered_data_column_types():
    df = pd.read_csv("data/03_engineered/engineered_data.csv")
    #clean_to_df = clean_data(df)
    expected_dtypes = {
        'Rotational speed [rpm]': np.int64,
        'Torque [Nm]': np.float64,
        'Tool wear [min]': np.int64,
        'Target': np.int64,
        'Air temperature [C]': np.float64,
        'Process temperature [C]': np.float64,
        'is_low_quality': np.int64,
        'is_medium_quality': np.int64,
        'is_high_quality': np.int64,
        'temp_difference': np.float64,
        'normalized_torque': np.float64,
        'low_speed': np.int64,
        'medium_speed': np.int64,
        'high_speed': np.int64
    }
    assert df.dtypes.to_dict() == expected_dtypes


def test_clean_data_type():
    df = pd.read_csv("data/01_raw/predictive_maintenance.csv")
    clean_to_df = clean_data(df)
    assert isinstance(clean_to_df, pd.DataFrame)

@pytest.mark.slow
def test_clean_date_null():
    df = pd.read_csv("data/01_raw/predictive_maintenance.csv")
    df_transformed = clean_data(df)
    assert not df_transformed.isnull().any().any()

def test_feature_engineering_torque():
    df = pd.read_csv("data/02_clean/clean_data.csv")
    df_final = feature_engineering(df)
    assert(df_final["Torque [Nm]"].min() >= 0)

def test_clean_data_columns():
    df = pd.read_csv("data/01_raw/predictive_maintenance.csv")
    clean_to_df = clean_data(df)
    assert clean_to_df.shape[1] == 7

def test_binary_variables_values():
    df = pd.read_csv("data/02_clean/clean_data.csv")
    feature_to_df = feature_engineering(df)
    binary_columns = ['is_low_quality', 'is_medium_quality', 'is_high_quality',
                      'low_speed', 'medium_speed', 'high_speed', 'Target']
    for column in binary_columns:
        unique_values = feature_to_df[column].unique()
        assert set(unique_values).issubset({0, 1}), f"Unexpected values in {column}"

