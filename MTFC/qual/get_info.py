from scipy import stats as stats
import pandas
import matplotlib.pyplot as plt
import numpy as np

def get_data_from_csv(csv_file):
    # Read the csv file
    data = pandas.read_csv(csv_file)

    # Get the data from the csv file
    return data

def get_average_deaths_by_year_by_cause(data):
    # Get the average of the state
    average_deaths_by_year_by_cause = data.groupby(['Year','Cause of Death']).sum()
    data = get_data_from_csv("final_data.csv")
    #graph deaths by year by cause
    data.plot.scatter(x='Year',y='Deaths',marker="-")
    # data.plot(kind='scatter',x="Year",title='Average of the State',y="Deaths",c="Cause of Death")
    print(average_deaths_by_year_by_cause)

    # Plot the average of the stat
    # average_state.plot(kind='scatter',x="nonzero_claims",title='Average of the State',y="")
    # plt.show()
    # print(average_deaths_by_year_by_cause)
    print(average_deaths_by_year_by_cause['Deaths'])
    plt.scatter(average_deaths_by_year_by_cause['Deaths'],average_deaths_by_year_by_cause['Year'])
    return average_deaths_by_year_by_cause


def get_trends_for_sucide_per_state(data):
    # Get the average of the state
    # average_deaths_by_year_by_cause = data.groupby(['Year','Cause of Death']).sum()
    # data = get_data_from_csv("final_data.csv")
    # #graph deaths by year by cause
    # data.plot.scatter(x='Year',y='Deaths',marker="-")
    # # data.plot(kind='scatter',x="Year",title='Average of the State',y="Deaths",c="Cause of Death")
    # print(average_deaths_by_year_by_cause)

    # # Plot the average of the stat
    # # average_state.plot(kind='scatter',x="nonzero_claims",title='Average of the State',y="")
    # # plt.show()
    # # print(average_deaths_by_year_by_cause)
    # print(average_deaths_by_year_by_cause['Deaths'])
    # plt.scatter(average_deaths_by_year_by_cause['Deaths'],average_deaths_by_year_by_cause['Year'])
    # return average_deaths_by_year_by_cause
    # Get deaths by suicide
    for val in data:
        print(val)

if __name__ == "__main__":
    data = get_data_from_csv("Scenario+Phase+Data+2022_qual.csv")
    # final_data = get_average_deaths_by_year_by_cause(data)
    # final_data.to_csv("final_data.csv")
    get_trends_for_sucide_per_state(data)
    # get_average_state(data)