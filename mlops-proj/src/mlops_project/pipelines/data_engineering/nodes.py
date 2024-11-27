"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.8
"""

from sklearn.model_selection import train_test_split
import pandas as pd

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Node to clean the raw data."""
    cleaned_data = data.copy()
    
    # Drop unnecessary columns
    cleaned_data = cleaned_data.drop(["UDI", 'Product ID', 'Failure Type'], axis=1)
    
    # Remove rows with missing values
    cleaned_data = cleaned_data.dropna()
    
    # Convert temperature columns from Kelvin to Celsius
    cleaned_data['Air temperature [C]'] = cleaned_data['Air temperature [K]'] - 273.15
    cleaned_data['Process temperature [C]'] = cleaned_data['Process temperature [K]'] - 273.15
    cleaned_data = cleaned_data.drop(['Air temperature [K]', 'Process temperature [K]'], axis=1)
    
    # Remove negative torque values
    cleaned_data = cleaned_data[cleaned_data['Torque [Nm]'] >= 0]
    
    return cleaned_data

def feature_engineering(cleaned_data: pd.DataFrame) -> pd.DataFrame:
    """Node to perform feature engineering."""
    engineered_data = cleaned_data.copy()

    # Create binary variables for product quality variants (L, M, H)
    engineered_data["is_low_quality"] = engineered_data['Type'].apply(lambda x: 1 if x.endswith("L") else 0)
    engineered_data["is_medium_quality"] = engineered_data['Type'].apply(lambda x: 1 if x.endswith("M") else 0)
    engineered_data["is_high_quality"] = engineered_data['Type'].apply(lambda x: 1 if x.endswith("H") else 0)

    engineered_data= engineered_data.drop('Type', axis=1)

    # Calculate the difference between air temperature and process temperature
    engineered_data["temp_difference"] = engineered_data['Air temperature [C]'] - engineered_data["Process temperature [C]"]

    # Normalize torque values by dividing by the maximum torque
    max_torque = engineered_data["Torque [Nm]"].max()
    engineered_data["normalized_torque"] = engineered_data["Torque [Nm]"] / max_torque

    # Create categorical variables for different rotational speed ranges
    engineered_data["low_speed"] = engineered_data['Rotational speed [rpm]'].apply(lambda x: 1 if x < 1000 else 0)
    engineered_data["medium_speed"] = engineered_data['Rotational speed [rpm]'].apply(lambda x: 1 if 1000 <= x < 2000 else 0)
    engineered_data["high_speed"] = engineered_data['Rotational speed [rpm]'].apply(lambda x: 1 if x >= 2000 else 0)

    return engineered_data



def split_data(engineered_data: pd.DataFrame) -> pd.DataFrame:
    """Node to split the data into train and test sets."""
    # Split the data into train and test sets

    y = pd.DataFrame(engineered_data['Target'])
    X = engineered_data.drop('Target', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

    return X_train, X_test, y_train, y_test 



