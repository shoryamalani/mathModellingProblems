import pandas
from wwo_hist import retrieve_hist_data
import sys
import os
os.chdir("./data")


frequency=24
start_date = '1-APR-2018'
end_date = '31-DEC-2019'
# api_key = 'd6a5e117670c4830b35192624221011'
api_key = "18e5bae3441f4d78b67200704221111"
location_list = ["Alabama",] # Get all states
all_states_list = pandas.read_csv("../disease_data/disease_1-3_2022.csv")["State"].values
final_state_list = []
for state in all_states_list:
    state = state.replace(".", "")
    state = state.replace(":", "")
    state = state.rstrip()
    state = state.replace(" ", "-")

    final_state_list.append(state)
final_state_list.remove("United-States")
final_state_list.remove("Other-States-5/")
def api_weather_data(location_list):
    final_location_list = []
    for location in location_list:
        if location+".csv" not in os.listdir():
            final_location_list.append(location)
    hist_weather_data = retrieve_hist_data(api_key,
                                    final_location_list,
                                    start_date,
                                    end_date,
                                    frequency,
                                    location_label = False,
                                    export_csv = True,
                                    store_df = True)
    return hist_weather_data

def get_weather_data(location):
    if os.path.exists(f"{location}.csv"):
        weather_data = pandas.read_csv(f"{location}.csv")
        return weather_data
    if __name__ != "__main__":
        weather_data = api_weather_data([location])
        return weather_data

def compile_disease_data():
    disease_data = {}
    data_files = ["disease_1-3_2022.csv", "disease_4-6_2022.csv", "disease_7-9_2021.csv", "disease_10-12_2021.csv"]
    ignore_columns = ["State","January 1 colonies","April 1 colonies","July 1 colonies","October 1 colonies","Maximum colonies","Lost colonies","Percent lost","Added colonies","Renovated colonies","Percent renovated","Other","Unkown"]
    for file in data_files:
        currentFile = pandas.read_csv("../disease_data/"+file)
        for disease in currentFile:
            if disease not in ignore_columns:
                avg = getAverageOfListWithErrors(currentFile[disease].values)
                if disease not in disease_data:
                    disease_data[disease] = {}
                for index, row in currentFile.iterrows():
                    stateName = row["State"]
                    stateName = stateName.replace(".", "")
                    stateName = stateName.replace(":", "")
                    stateName = stateName.rstrip()
                    try:
                        if row[disease] == "-":
                            val = 0
                        else:
                            row[disease] = float(row[disease])
                            val = row[disease]
                        if stateName not in disease_data[disease]:
                            disease_data[disease][stateName] = [val]
                        else:
                            disease_data[disease][stateName].append(val)
                        
                    except:
                        if stateName not in disease_data[disease]:
                            disease_data[disease][stateName] = [avg]
                        else:
                            disease_data[disease][stateName].append(avg)
                        
    return disease_data
                        
def getAverageOfListWithErrors(data):
    tot = 0
    totNum = 0
    for a in data:
        try:
            if a == "-":
                a = 0
            if type(a) == str:
                a = a.replace(",", "")
            a = float(a)
            tot +=a
            totNum+=1
        except:
            pass
    return tot/totNum

# def compile_weather_csvs():
#     final_data = {}
#     for state in final_state_list:
#         final_data[state] =  get_weather_data(state)
#     pandas.DataFrame(final_data).to_csv("weather_data.csv")

import os
import csv, glob
def compile_weather_csvs():
    Dir = "."
    Avg_Dir = "../average_data"

    csv_file_list = sorted(glob.glob(os.path.join(Dir, '*.csv'))) # returns the file list
    print (csv_file_list)

    with open(os.path.join('../Output.csv'), 'w', newline='') as f:
        wf = csv.writer(f, lineterminator='\n')

        for files in csv_file_list:
            with open(files, 'r') as r: 
                next(r)                   # SKIP HEADERS
                rr = csv.reader(r)
                for row in rr:
                    wf.writerow(row)
if __name__ == "__main__":
    compile_weather_csvs()
    # api_weather_data(final_state_list)
    # print(final_state_list)
    # compile_disease_data()