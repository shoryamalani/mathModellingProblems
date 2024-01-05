# statscast_woba.py
# grab data from statscast
# predict woba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

DATA_PATH = 'data'
# read in data
def get_data(data_file='statscast_data.csv'):
    with open(os.path.join(DATA_PATH,data_file)) as f:
        df = pd.read_csv(f)
    return df

def set_up_prediction_model(data):
    # set up data for prediction
    # drop columns
    data = data.drop(["Team"], axis=1)
    # set up X and y
    X = data.drop(['WOBA'], axis=1)
    y = data['WOBA']
    # split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # set up model
    model = LinearRegression()
    model.fit(X_train, y_train)
    # predict
    y_pred = model.predict(X_test)
    # evaluate model
    print('Coefficients: \n', model.coef_)
    print('Mean squared error: %f'
            % mean_squared_error(y_test, y_pred))
    return model


def predict_using_model(model,data):
    # predict using model
    # drop columns
    data = data.drop(["Team"], axis=1)
    # set up X and y
    X = data.drop(['WOBA'], axis=1)
    y = data['WOBA']
    # predict
    y_pred = model.predict(X)
    # evaluate model
    print(y)
    print(y_pred)
    print('Mean squared error: %f'
            % mean_squared_error(y, y_pred))
    return y_pred



if __name__ == '__main__':
    data = get_data()
    model = set_up_prediction_model(data)    
    test_data = get_data('statscast_test_data.csv')
    y_pred = predict_using_model(model,test_data)

