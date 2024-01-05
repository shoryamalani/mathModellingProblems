import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing
import statsmodels.api as ssm

# Read the data
data = pandas.read_csv('Final_Exam_Data.csv')

# Split the data into X and Y
Y = data['Wins']
X = data.drop(['Wins'], axis=1)
X = X.drop(['Team'], axis=1)
X = X.drop(['H_2B'], axis=1)
X = X.drop(['H_1B'], axis=1)
X = X.drop(['Year'], axis=1)
X = X.drop(['H_BA'], axis=1)
X = X.drop(['H_3B'], axis=1)
# X = ssm.add_constant(X)
print(X.head())
print(Y.head())


lin_reg = ssm.OLS(Y, X).fit()
print(lin_reg.summary())
print(lin_reg.pvalues)


