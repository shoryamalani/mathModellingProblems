import pandas
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import OLSInfluence
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('seaborn')

def read_csv(file):
    # Read in the data
    data = pandas.read_csv(file)
    return data

def main():
    # Read in the data
    df = read_csv("data/city_temps.csv")
    numpy_array = df.to_numpy()
    
    lin_reg = LinearRegression()
    lin_reg.fit(numpy_array[:, 1].reshape(-1, 1), numpy_array[:, 2])
    print(lin_reg.coef_)
    # plt.text(170, 95, 'y = {:.2f} + {:.2f} * x'.format(lin_reg.intercept_, lin_reg.score(numpy_array[:, 1].reshape(-1, 1), numpy_array[:, 2])), fontsize=16, color='red')
    predicted_temp = lin_reg.predict(df[['LAT']])
    ax = sns.scatterplot(y='TEMP',x='LAT',data=df)
    sns.regplot(y='TEMP',x='LAT',data=df)
    
    print(lin_reg.intercept_)
if __name__ == "__main__":
    main()