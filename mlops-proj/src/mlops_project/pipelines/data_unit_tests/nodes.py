"""
This is a boilerplate pipeline 'data_unit_tests'
generated using Kedro 0.18.8
"""

import logging
import pandas as pd
import great_expectations as ge

def unit_test(data: pd.DataFrame, ):

    pd_df_ge = ge.from_pandas(data)

    assert pd_df_ge.expect_column_values_to_be_of_type('Type', 'str').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Air temperature [K]', 'float').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Process temperature [K]', 'float').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Rotational speed [rpm]', 'int').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Type', 'str').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Torque [Nm]', 'float').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Target', 'int').success == True
    assert pd_df_ge.expect_column_values_to_be_of_type('Failure Type', 'str').success == True

    # log = logging.getLogger(__name__)
    # log.info('Data passed on the unit tests')

    return 0