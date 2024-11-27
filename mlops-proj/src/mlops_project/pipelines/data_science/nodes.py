"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.8
"""
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import pandas as pd
import mlflow
import logging


def train_model(X_train, y_train):
    """Node to train a machine learning model."""

    mlflow.autolog(log_input_examples=True,log_model_signatures=True)
    model = RandomForestClassifier(n_estimators=150, random_state=0)
    model.fit(X_train, y_train)

    return model

def predict(ml_model, X_test, y_test):
    """Node to make predictions using a trained model."""

    y_pred = ml_model.predict(X_test)

    y_pred = pd.DataFrame(y_pred, columns=['y_pred'])

    f1_score_value = f1_score(y_test, y_pred)

    log = logging.getLogger(__name__)
    log.info("Model F1-score on test set: %0.2f%%", f1_score_value)

    
    return y_pred