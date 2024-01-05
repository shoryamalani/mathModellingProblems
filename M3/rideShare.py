import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

import datetime
import json
import math
import typing
import multiprocessing

import constants
import helpers 

import capitalBikeShare
import bingDistance



np.random.seed(constants.random_seed)


def get_distance_of_trip(start_coords, end_coords, time):
    return constants.trip_avg_official_speed * time / 3600 
    # if start_coords == end_coords:
    #     distance = constants.trip_avg_official_speed * time
    # else:
    #     name = str(start_coords)+"/"+str(end_coords)
    #     if name in constants.memoized_distances:
    #         return constants.memoized_distances[name]
    #     else:
    #         distance = bingDistance.get_distance_between_coords(start_coords[0],start_coords[1], end_coords[0], end_coords[1])
    #         if distance is None:
    #             distance = constants.trip_avg_official_speed * time
    #         constants.memoized_distances[name] = distance
    # return distance

def add_to_memoized_distances_file():
    with open(constants.memoized_distances_file_path, "w") as f:
        json.dump(constants.memoized_distances, f)
    
def add_to_memoized_locations_file():
    with open(constants.memoized_location_file_path, "w") as f:
        json.dump(constants.memoized_locations, f)


def get_log_lat_of_place(place):
    memoized_locations = json.load(open(constants.memoized_location_file_path))
    if place in memoized_locations:
        memoized_locations[str(place)]
    else:
        return None


def save_all_long_lat():
    # datetime go month by month from 2019 to 2023
    # add multiple processes to get the data

    time = datetime.datetime(2022, 4, 1, 0, 0, 0)
    month = datetime.timedelta(days=30)
    end_time = datetime.datetime(2023, 2, 1, 0, 0, 0)
    full_long_lat = {}
    # add 10 processes
    
    while time < end_time:
        cur_long_lat = capitalBikeShare.get_month_of_year(time.strftime("%Y"), time.strftime("%m"))
        # go through each row and get the start_station_id and end_station_id and see if they are in the full_long_lat
        # if they are not, then add them
        for index, row in cur_long_lat.iterrows():
            # check if start_station_id is in full_long_lat
            if row["start_station_id"] not in full_long_lat:
                # add the row to full_long_lat
                full_long_lat[str(row["start_station_id"])] = {"lat": row["start_lat"], "long": row["start_lng"]}
            # check if end_station_id is in full_long_lat
            if row["end_station_id"] not in full_long_lat:
                # add the row to full_long_lat
                full_long_lat[str(row["end_station_id"])] = {"lat": row["start_lat"], "long": row["end_lng"]}
        print(time.strftime("%Y"), time.strftime("%m") + " done")
        time = time + month

        # date = capitalBikeShare.get_month_of_year(start_time.year, start_time.month)
    # save the full_long_lat to a memoized_location file
    with open(constants.memoized_location_file_path, "w") as f:
        json.dump(full_long_lat,f)
    return None
        

def get_monthly_and_quarterly_data():
    time = constants.capitalBikeShare_start_time_quarterly
    add = datetime.timedelta(days=90)
    end_time = constants.capitalBikeShare_start_time_monthly
    sampled_date = {}
    while time < end_time:
        data = capitalBikeShare.get_quarterly_with_year(time.year, math.ceil(time.month/3))
        sample = capitalBikeShare.get_sample_of_monthly_data(data,constants.sample_size)
        time = time + add
        print(time.year, time.month)
        sampled_date[time] = sample
    time = constants.capitalBikeShare_start_time_monthly
    end_time = constants.capitalBikeShare_start_time_end
    add = datetime.timedelta(days=30)
    while time < end_time:
        data = capitalBikeShare.get_month_of_year(time.year, time.month)
        sample = capitalBikeShare.get_sample_of_monthly_data(data,constants.sample_size)
        time = time + add
        print(time.year, time.month)
        sampled_date[time] = sample
    return sampled_date
def add_points_to_memoization(points, coords):
    for point in points:
        if point not in constants.memoized_locations:
            constants.memoized_locations[point] = {"lat":coords[points.index(point)][0], "long":coords[points.index(point)][1]}
    with open(constants.memoized_location_file_path, "w") as f:
        json.dump(constants.memoized_locations, f)
    
    

def get_distance_of_dates(data : typing.Dict[float, typing.List[capitalBikeShare.CapitalBikeRide]]):
    cur = 0
    global constants
    for key, values in data.items():
        for a in values:
            # start_coords = get_log_lat_of_place(a.start_station_id)
            # end_coords = get_log_lat_of_place(a.end_station_id)
            # if start_coords is None or end_coords is None:
            #     if start_coords is None:
            #         start_coords =  capitalBikeShare.geocode_location(a.start_station_name)
            #     if end_coords is None:
            #         end_coords = capitalBikeShare.geocode_location(a.end_station_name)
            #     if start_coords is None or end_coords is None:
            #         continue
            #     add_points_to_memoization([a.start_station_id, a.end_station_id], [start_coords, end_coords])
            
            # if start_coords[0] < end_coords[0]:
            #     start_coords, end_coords = end_coords, start_coords
            cur += 1
            # distance = get_distance_of_trip(start_coords,end_coords, a.duration)
            distance = get_distance_of_trip([],[] , a.duration)
            a.distance = distance
            if cur % 20 == 0:
                add_to_memoized_distances_file()
    return data

def make_all_locations_int():
    for key, value in constants.memoized_locations.items():
        if type(key) == list:
            del constants.memoized_locations[key]
    with open(constants.memoized_location_file_path, "w") as f:
        json.dump(constants.memoized_locations, f)

def get_average_distance_by_dates(data):
    vals = []
    for key, values in data.items():
        total = 0
        for value in values:
            total += value.distance
        vals.append(total/len(values))
    return vals
    

if __name__ == "__main__":
    # data = capitalBikeShare.get_month_of_year("2019", "01")
    # print(data.head())
    # locations = json.load(constants.memoized_location_file_path)
    # save_all_long_lat()
    origin_data = get_monthly_and_quarterly_data()
    # data= {"a": capitalBikeShare.get_sample_of_monthly_data(capitalBikeShare.get_month_of_year("2019", "01"), 0.01)}
    data = get_distance_of_dates(origin_data)

    data = get_average_distance_by_dates(data)
    print(data)
    data = [helpers.distance_traveled_to_emissions_saved(x) for x in data]

    # make_all_locations_int()
    