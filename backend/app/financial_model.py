import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_financial_model(df):
    """Train the financial model Random Forest"""

    x = df.drop('label', axis=1)
    y = df['label']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x,y)
    return model

def predict_financial(model, data):
    return model.predict(data)