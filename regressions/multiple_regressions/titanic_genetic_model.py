import pygad
import numpy
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
"""
Given the following function:
    y = f(w1:w6) = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + 6wx6
    where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7) and y=44
What are the best values for the 6 weights (w1 to w6)? We are going to use the genetic algorithm to optimize this function.
"""
def read_csv(file):
    # Read in the data
    data = pandas.read_csv(file)
    return data
def fix_data(data):
    data.drop('Name',axis= 1, inplace= True)
    data.drop('Ticket',axis= 1, inplace= True)
    data.drop('Cabin',axis= 1, inplace= True)
    # df.drop('Embarked',axis= 1, inplace= True)
    data.drop('PassengerId',axis= 1, inplace= True)
    data.drop('Parch',axis= 1, inplace= True)
    data.drop('SibSp',axis=1,inplace=True)
    # df.drop('Pclass',axis= 1, inplace= True
    data.fillna(data.mean(), inplace=True)
    # creating x variables and y output
    if 'Survived' in data:
        x = data.drop('Survived',axis= 1,)
    else:
        x = data
    x = ssm.add_constant(x)
    for a in x['Sex']:
        if a == 'male':
            s = 0
        if a == 'female':
            s = 1
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
    # x.drop('PassengerId',axis= 1, inplace= True)
    # x.drop('Name',axis= 1, inplace= True)
    # x.drop('Ticket',axis= 1, inplace= True)
    # x.drop('Cabin',axis= 1, inplace= True)
    # x.drop('Embarked',axis= 1, inplace= True)
    # x.drop('Parch',axis= 1, inplace= True)
    # x.drop('SibSp',axis=1,inplace=True)
    if 'Survived' in data:
        y = data['Survived']
    else:
        y = None
    return x,y

data = read_csv("titanic/train.csv")
x_data,y_data = fix_data(data)
lin_reg_test = LinearRegression()

function_inputs = [-0.15583874, -0.64929309,  1.18149204, -0.0307999,  -0.01344411, -0.24350789]
desired_output = 44 # Function output.

def fitness_func(solution, solution_idx):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    # X_train, X_test, Y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)

    # lin_reg_test = LinearRegression(n_jobs=10)
    # lin_reg_test.fit(X_train,Y_train)
    # print(lin_reg_test.coef_)
    # predictions = lin_reg_test.predict(X_test)
    # return  1- mean_absolute_error(y_test, predictions)
    model = ssm.OLS(y_data, x_data.astype(float))
    predictions = model.predict(solution)
    predictions = [round(num) for num in predictions]
    score = 0
    for i in range(len(predictions)):
        if predictions[i] == y_data[i]:
            score += 1
    return score/len(predictions)

fitness_function = fitness_func

num_generations = 20 # Number of generations.
num_parents_mating = 45 # Number of solutions to be selected as parents in the mating pool.

# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 250 # Number of solutions in the population.
num_genes = len(function_inputs)

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop, 
                       num_genes=num_genes,
                       on_generation=callback_generation,
                       mutation_num_genes=3,
                    #    parallel_processing=["thread",2],
                    #    random_mutation_max_val=0.0005,
                    #    random_mutation_min_val=-0.0005,
                    #    gene_space=[-0.15, -0.6,  1.2, -0.034,  -0.06, -0.1],
                        init_range_low=-0.6,
                        init_range_high=1.6,

                    # keep_parents=-1,
                    # save_best_solutions=True
                       )

# Running the GA to optimize the parameters of the function.
ga_instance.run()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
# ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
test_set = read_csv("titanic/test.csv")
passenger_ids = test_set['PassengerId']
x_data,y_data_new = fix_data(test_set)
model = ssm.OLS(passenger_ids, x_data.astype(float))
predictions = model.predict(solution)
predictions = [round(num) for num in predictions]
ouput = pandas.DataFrame({'PassengerId': passenger_ids, 'Survived': predictions})
ouput.to_csv("data/ouput.csv", index= False)
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

# prediction = numpy.sum(numpy.array(function_inputs)*solution)
# print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

# if ga_instance.best_solution_generation != -1:
#     print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

# # Saving the GA instance.
# filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
# ga_instance.save(filename=filename)

# # Loading the saved GA instance.
# loaded_ga_instance = pygad.load(filename=filename)
# loaded_ga_instance.plot_fitness()