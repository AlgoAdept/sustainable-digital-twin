import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train_model():
    df = pd.read_csv('data/mock_training_data.csv')

    X = df[['inventory', 'expiry_days', 'carbon_score']]
    y = df['donation_likelihood']

    model = LogisticRegression()
    model.fit(X, y)
    return model

def predict_donation(model, inventory, expiry_days, carbon_score):
    input_data = [[inventory, expiry_days, carbon_score]]
    return model.predict(input_data)[0]
