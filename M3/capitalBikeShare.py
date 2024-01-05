import pandas as pd
import constants
import os 
from datetime import datetime
import requests
import APIKEYS
class CapitalBikeRide:
    distance = None
    def __init__(self, start_station_id, end_station_id, start_time, end_time, duration, start_station_name, end_station_name):
        self.start_station_id = start_station_id
        self.end_station_id = end_station_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.start_station_name = start_station_name
        self.end_station_name = end_station_name


def get_month_of_year(year, month):
    # join two paths
    if int(year) < 2018:
        raise ValueError("Data not available for this year")
    folder =constants.capitalBikeShare_data_file_path
    if month < 10:
        month = "0" + str(month)
    fileName =str(year) + str(month) + "-capitalbikeshare-tripdata.csv"
    data = pd.read_csv(os.path.join(folder, fileName))
    return data

def get_quarterly_with_year(year, quarter):
    # join two paths
    if int(year) > 2019:
        raise ValueError("Quaterly Data not available for this year")
    folder =constants.capitalBikeShare_data_file_path + "/" + str(year)  + "-capitalbikeshare-tripdata"
    fileName =str(year) + "Q"+ str(quarter) + "-capitalbikeshare-tripdata.csv"
    data = pd.read_csv(os.path.join(folder, fileName))
    return data

def get_sample_of_monthly_data(start_data, sample_size):
    df = start_data.sample(frac=sample_size)
    sample = []
    for index, row in df.iterrows():
        if "Duration" in row:
            sample.append(CapitalBikeRide(row["Start station number"], row["End station number"], row["Start date"], row["End date"], (datetime.strptime(row["End date"], constants.date_format)-datetime.strptime(row["Start date"], constants.date_format)).seconds, row["Start station"], row["End station"]))
        else:
            sample.append(CapitalBikeRide(row["start_station_id"], row["end_station_id"], row["started_at"], row["ended_at"], (datetime.strptime(row["ended_at"], constants.date_format)-datetime.strptime(row["started_at"], constants.date_format)).seconds, row["start_station_name"], row["end_station_name"]))
    return sample
def geocode_location(place):
    # use position stack to geocode
    # https://positionstack.com/documentation
    place = str("Washington DC,") + place
    data = requests.get(f"http://api.positionstack.com/v1/forward?access_key={APIKEYS.position_stack}&query={place}")
    data = data.json()
    if data["data"] == []:
        return None
    if data["data"][0] == []:
        return None
    data = data["data"][0]
    return [data["latitude"], data["longitude"]]

    
