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
    df = read_csv("data/temps_train.csv")
    numpy_array = df.to_numpy()
    # creating feature variables
    x = df.drop('TEMP',axis= 1)
    x.drop('Place',axis= 1, inplace= True)
    x.drop('POPN',axis= 1, inplace= True)
    x.drop("RAIN_IN",axis=1,inplace=True)
    for val in x["ELEV_FT"]:
        if "," in val:
            x["ELEV_FT"].replace({val: val.replace(',',"")}, inplace= True)
    y = df['TEMP']
    print(x)
    print(y)
    # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.9, random_state=101)

    # lin_reg = LinearRegression(n_jobs=10)
    # lin_reg.fit(X_train,y_train)
    # print(lin_reg.coef_)
    # predictions = lin_reg.predict(X_test)
    # plt.text(170, 95, 'y = {:.2f} + {:.2f} * x'.format(lin_reg.intercept_, lin_reg.score(numpy_array[:, 1].reshape(-1, 1), numpy_array[:, 2])), fontsize=16, color='red')
    # print('mean_squared_error : ', mean_squared_error(y_test, predictions))
    # print('mean_absolute_error : ', mean_absolute_error(y_test, predictions))
    x = ssm.add_constant(x)
    lin_reg = LinearRegression(n_jobs=10)
    lin_reg.fit(x,y)
    print(lin_reg.intercept_)
    model = ssm.OLS(y, x.astype(float))
    results = model.fit()
    print(results.summary())
    test_set = read_csv("data/temps_test.csv")
    test_set.drop('Place',axis= 1, inplace= True)
    # test_set.drop('POPN',axis= 1, inplace= True)
    for val in test_set["ELEV_FT"]:
        if type(val) == str:
            if "," in val:
                test_set["ELEV_FT"].replace({val: val.replace(',',"")}, inplace= True)
    test_set.drop('TEMP',axis= 1, inplace= True)
    test_set = ssm.add_constant(test_set)
    predictions = lin_reg.predict(test_set)
    #return values to csv
    test_set = read_csv("data/temps_test.csv")
    test_set['TEMP'] = predictions
    test_set.to_csv("data/temps_test.csv", index= False)
        
    print(predictions)


if __name__ == "__main__":
    main()