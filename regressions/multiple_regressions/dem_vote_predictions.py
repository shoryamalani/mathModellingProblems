import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing
import statsmodels.api as ssm
plt.style.use('seaborn')

def read_csv(file):
    # Read in the data
    data = pandas.read_csv(file)
    return data


def main():
    # Read in the data
    df = read_csv("data/politics_train.csv")
    numpy_array = df.to_numpy()
    # creating x variables and y output
    x = df.drop('VOTE',axis= 1)
    x.drop('STATE',axis= 1, inplace= True)
    x.drop('Locality',axis= 1, inplace= True)
    y = df['VOTE']
    print(x)
    # print(y)
    
    lin_reg = LinearRegression(n_jobs=10)
    lin_reg.fit(x,y)
    # print(lin_reg.intercept_)
    x = ssm.add_constant(x)
    model = ssm.OLS(y, x.astype(float))
    results = model.fit()
    # print(results.summary())
    # test data
    test_set = read_csv("data/politics_test.csv")
    test_set.drop('STATE',axis= 1, inplace= True)
    test_set.drop('Locality',axis= 1, inplace= True)
    if 'VOTE' in test_set.columns:
        test_set.drop('VOTE',axis= 1, inplace= True)
    print(test_set)
    # test_set = ssm.add_constant(test_set)
    predictions = lin_reg.predict(test_set)
    #return values to csv
    test_set = read_csv("data/politics_test.csv")
    test_set['VOTE'] = predictions
    test_set.to_csv("data/politics_test.csv", index= False)


if __name__ == "__main__":
    main()