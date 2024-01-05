from operator import truediv
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
    df = read_csv("titanic/train.csv")
    numpy_array = df.to_numpy()
    df.drop('Name',axis= 1, inplace= True)
    df.drop('Ticket',axis= 1, inplace= True)
    df.drop('Cabin',axis= 1, inplace= True)
    df.drop('Fare',axis= 1, inplace= True)
    df.drop('PassengerId',axis= 1, inplace= True)
    df.drop('Parch',axis= 1, inplace= True)
    # df.drop('SibSp',axis=1,inplace=True)
    # df.drop('Pclass',axis= 1, inplace= True)
    # df.drop("Sex",axis=1,inplace=True)
    # df.dropna(inplace=True)
    df.fillna(df.mean(), inplace=True)
    # creating x variables and y output
    x = df.drop('Survived',axis= 1,)
    x = ssm.add_constant(x)
    # x.drop('PassengerId',axis= 1, inplace= True)
    # x.drop('Name',axis= 1, inplace= True)
    # x.drop('Ticket',axis= 1, inplace= True)
    # x.drop('Cabin',axis= 1, inplace= True)
    # x.drop('Embarked',axis= 1, inplace= True)
    for a in x['Sex']:
        if a == 'male':
            s = 1
        if a == 'female':
            s = 3
        x["Sex"].replace({a: s}, inplace= True)
    for a in x["Embarked"]:
        s = None
        if a == 'S':
            s = 1
        elif a == 'C':
            s = 2
        elif a == 'Q':
            s = 3
        else:
            s = a
        x["Embarked"].replace({a: s}, inplace= True)
        
    x.fillna(x.mean(),inplace=True)
    


    y = df['Survived']
    print(x)
    X_train, X_test, Y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)

    lin_reg_test = LinearRegression(n_jobs=10)
    lin_reg_test.fit(X_train,Y_train)
    print(lin_reg_test.coef_)
    predictions = lin_reg_test.predict(X_test)
    # plt.text(170, 95, 'y = {:.2f} + {:.2f} * x'.format(lin_reg_test.intercept_, lin_reg_test.score(numpy_array[:, 1].reshape(-1, 1), numpy_array[:, 2])), fontsize=16, color='red')
    print('mean_squared_error : ', mean_squared_error(y_test, predictions))
    print('mean_absolute_error : ', mean_absolute_error(y_test, predictions))
    print(y)
    lin_reg = LinearRegression(n_jobs=10)
    lin_reg.fit(x,y)
    
    # print(lin_reg.intercept_)
    model = ssm.OLS(y, x.astype(float))
    results = model.fit()
    print(results.summary())
    # test data
    test_set = read_csv("titanic/test.csv")
    test_set = ssm.add_constant(test_set)
    test_set.drop('PassengerId',axis= 1)
    test_set.drop('Name',axis= 1, inplace= True)
    test_set.drop('Ticket',axis= 1, inplace= True)
    test_set.drop('Cabin',axis= 1, inplace= True)
    # test_set.drop('Embarked',axis= 1, inplace= True)
    test_set.drop('Parch',axis= 1, inplace= True)
    # test_set.drop('SibSp',axis=1,inplace=True)
    # test_set.drop('Pclass',axis= 1, inplace= True)
    # test_set.drop('Sex',axis=1,inplace=True)
    test_set.drop("Fare",axis=1,inplace=True)

    for a in test_set['Sex']:
        if a == 'male':
            s = 1
        if a == 'female':
            s = 3
        test_set["Sex"].replace({a: s}, inplace= True)
    for a in test_set["Embarked"]:
        s = None
        if a == 'S':
            s = 1
        elif a == 'C':
            s = 2
        elif a == 'Q':
            s = 3
        else:
            s = a
        test_set["Embarked"].replace({a: s}, inplace= True)
    test_set.fillna(test_set.mean(),inplace=True)
    
    print(test_set)
    # test_set = ssm.add_constant(test_set)
    predictions = results.predict(test_set.drop('PassengerId',axis= 1))
    final_predictions = []
    for prediction in predictions:
        prediction = round(prediction)
        final_predictions.append(prediction)
    #return values to csv
    ouput = pandas.DataFrame({'PassengerId': test_set.PassengerId, 'Survived': final_predictions})
    ouput.to_csv("data/ouput.csv", index= False)


if __name__ == "__main__":
    main()