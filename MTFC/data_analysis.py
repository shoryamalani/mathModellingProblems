from scipy import stats as stats
import pandas
import matplotlib.pyplot as plt
import numpy as np

def get_data_from_csv(csv_file):
    # Read the csv file
    data = pandas.read_csv(csv_file)

    # Get the data from the csv file
    return data

def get_average_state(data):
    # Get the average of the state
    average_state = data.groupby('region').mean()
    print(average_state)

    # Plot the average of the stat
    # average_state.plot(kind='scatter',x="nonzero_claims",title='Average of the State',y="")
    # plt.show()
    print(average_state)

def get_nebraska_no_preventitive_measures(data):
    # Get the data for nebraska
    nebraska = data[data['region'] == 'Nebraska']
    # Get the data for nebraska that has no preventitive measures
    nebraska_no_preventitive_measures = nebraska[nebraska['prev_measures'] == 'no']
    # Get the average of the data for nebraska that has no preventitive measures
    claim_num =0
    for claim in nebraska_no_preventitive_measures['nonzero_claims']:
        if claim > 14000:
            claim_num+=1
    print(claim_num/len(nebraska_no_preventitive_measures['nonzero_claims']))
    # average_nebraska_no_preventitive_measures = nebraska_no_preventitive_measures.mean()
    # print(average_nebraska_no_preventitive_measures)
def get_illinois_diff_prev(data):
    # get data for illinois
    illinois = data[data['region'] == 'Illinois']
    # get expected value for preventitive measures
    illinois_prev = illinois[illinois['prev_measures'] == 'yes']
    illinois_prev_mean = illinois_prev.mean()[2]
    # get expected value for no preventitive measures
    illinois_no_prev = illinois[illinois['prev_measures'] == 'no']
    illinois_no_prev_mean = illinois_no_prev.mean()[2]
    # get difference
    diff = illinois_prev_mean - illinois_no_prev_mean
    return diff
#make regression with elevation and claims
def get_regression(data):
    # get data for elevation and claims
    elevation = data['elevation']
    claims = data['nonzero_claims']
    # get regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(elevation, claims)
    predict = slope * 2000 + intercept
    return slope, intercept, r_value, p_value, std_err,predict

def main():
    data = get_data_from_csv("data/floodData.csv")
    # get_average_state(data)
    # get_nebraska_no_preventitive_measures(data)
    diff = get_illinois_diff_prev(data)
    print(diff)
    slope, intercept, r_value, p_value, std_err,predict = get_regression(data)
    print(slope, intercept, r_value, p_value, std_err,predict)
if __name__ == "__main__":
    main()