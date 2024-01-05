import requests
import APIKEYS
import ratelimiter
from ratelimiter import RateLimiter
from random import random
cur_key = 0
def get_distance_between_coords(lat1, long1, lat2, long2):
    # get the distance between two coordinates from bing
    global cur_key
    data = requests.get(f"http://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={lat1},{long1}&destinations={lat2},{long2}&travelMode=driving&key={APIKEYS.bing_map_api_key[cur_key]}")
    cur_key = (cur_key + 1) % len(APIKEYS.bing_map_api_key)
    try:
        distance = data.json()['resourceSets'][0]['resources'][0]['results'][0]['travelDistance']
    except:
        distance = None

    return distance

    

def test_get_distance_between_coords():
    """
    tests the function, "get_distance_between_coords"
    """
    print(get_distance_between_coords(47.6044,-122.3345,47.6731,-122.1185))

if __name__ == "__main__":
    test_get_distance_between_coords()


# using sales numbers to estimate ownership and usage
import pandas as pd
import constants

sales_data_in_thousands = pd.Series({2012:70,
2013:159,
2014:193,
2015:130,
2016:152,
2017:(152 + 369) /2, # imputing the average between the two
2018:369,
2019:423,
2020:416,
2021:750,
2022:928,
})
sales_data_in_thousands = pd.DataFrame(sales_data_in_thousands)



def aggregate_sales_numbers(sales_data: pd.DataFrame):
    """
    We are assuming that a total number of ebike sales is a good number for owners
    """
    return_df = sales_data.copy()
    running_total = 0
    totals = []
    for x,y in sales_data.iterrows():
        running_total += y[0]
        print(x,y[0])
        totals.append(running_total)
    return totals


def aggregate_miles_traveled_by_owners_yearly(ownership_data) -> pd.DataFrame:
    """
    getting the aggregate data traveled by owners yearly
    ownership data: ownership data in thousands
    """
    final = []
    data_f = {

    }
    year = 2012
    for val in ownership_data:
        num_riding_miles = val * constants.avg_miles_covered_per_day_by_ebike_owners * 365.25 * 1000 # num minutes covered in a year
        data_f[year] = num_riding_miles
        year += 1
    return data_f

ownership_data_in_thousands = aggregate_sales_numbers(sales_data_in_thousands)
print(ownership_data_in_thousands)

aggregate_miles_traveled_by_owners = aggregate_miles_traveled_by_owners_yearly(ownership_data_in_thousands)
print(aggregate_miles_traveled_by_owners)
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
    
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

import constants

if __name__ == "__main__":
    # Read in the data
    data = pd.read_csv(constants.BTS_data_file_path)

import pandas as pd
import constants
import datetime

def distance_traveled_to_emissions_saved(distance: float, distance_units='km') -> float: 
    """
    Takes the amount of distance and converts it to emissions saved based on percentage of cars and public transport saved
    this is generous because it assumes that not using public transport saves emissions, which it does not (over the short term at least)
    """

    if distance_units == 'km':
        distance = distance * constants.km_to_mile_multiplier

    net_carbon = distance * constants.ebike_mile_emissions

    carbon_otherwise = (constants.would_use_car * constants.car_mile_emissions + constants.would_use_public_transit * constants.bus_mile_emissions)*distance

    return carbon_otherwise - net_carbon

def get_total_carbon_emissions_saved_monthly(avg_distance_of_trip, month: datetime.datetime) -> float:
    """
    avg_distance_of_trip: distance of trip aggregated over month
    month: month in datetime

    returns estimated carbon emissions saved in tons

    We are assuming that no trip, bike rides, and walking emit 0.
    """
    return distance_traveled_to_emissions_saved(avg_distance_of_trip) * (constants.shared_ridership_total[month.year] / 12) * 1000

def get_total_carbon_emissions_saved_yearly(avg_distance_of_trip, year: datetime.datetime) -> float:
    """
    avg_distance_of_trip: distance of trip aggregated over month
    year: year in datetime

    returns estimated carbon emissions saved in tons

    We are assuming that no trip, bike rides, and walking emit 0.
    """
    return distance_traveled_to_emissions_saved(avg_distance_of_trip) * (constants.shared_ridership_total[year.year]) * 1000

def get_calorie_change_monthly(avg_distance_of_trip, year:datetime.datetime) -> float:
    """
    returns the total calorie change monthly
    """
    pass


def km_to_miles(distance: float) -> float:
    return distance * constants.km_to_mile_multiplier

def seconds_to_hours(seconds: float) -> float:
    return seconds / 3600

def hours_to_seconds(hours: float) -> float:
    return hours * 3600

def miles_to_km(distance: float) -> float:
    return distance * constants.mile_to_km_multiplier

import pandas as pd
import json
import datetime
#Datashare constants
BTS_data_file_path = "data/bikeOwnership/shareUsage.csv"



sample_size = 0.001

# Capital Bike Share constants
capitalBikeShare_data_file_path = "data/bikeShare/capitalBikeShare/"
memoized_location_file_path = "data/bikeShare/capitalBikeShare/memoized_location.json"
memoized_distances_file_path = "data/bikeShare/capitalBikeShare/memoized_distances.json"
memoized_locations = json.load(open(memoized_location_file_path, "r"))
memoized_distances = json.load(open(memoized_distances_file_path, "r"))
capitalBikeShare_start_time_quarterly = datetime.datetime(2012, 1, 1, 0, 0, 0)
capitalBikeShare_start_time_monthly = datetime.datetime(2018, 1, 1, 0, 0, 0)
capitalBikeShare_start_time_end = datetime.datetime(2023, 2, 1, 0, 0, 0)

# US data based on Knoxville 2012 -- PLEASE CITE
# survey question: if you didn't use an ebike, how would you go to your destination? percentage



# important constants for analysis
# https://www.sciencedirect.com/science/article/pii/S136192092030599X
# using the kentucky 2013 survey because no other surveys that are from north america and have all of the options
would_use_car = 0.11
would_use_public_transit = 0.11
would_use_normal_bike = 0.11
would_walk = 0.57
would_no_trip = 0.11

# mileage
# https://mobilitylab.org/2016/06/21/capital-bikeshare-gps-data-trips/
trip_avg_official_speed = 7.5 * 1.60934 # km/h

# https://www.cbo.gov/publication/58861
# WARNING THIS IS AN ASSUMPTION -- the carbon emissions offset by ebikes from cars can be estimated by the fuel usage of the average passenger vehicle
car_mile_emissions = 0.000445334
ebike_mile_emissions = 6.17294e-6
no_trip_mile_emissions = 0
bus_mile_emissions = 0.0002661 # THIS IS A TERRIBLE METRIC PLEASE DISCLOSE
# public transport passenger mile emissions


# https://ourworldindata.org/travel-carbon-footprint


# food consumption and energy
# healthiness ... 
# https://www.ebikes.ca/documents/Ebike_Energy.pdf
# energy consumption
# https://ebikeshq.com/electric-bikes-environment-carbon-footprint-energy-battery-disposal/

# in watt-hours
bike_ebike_energy_cost = 16.0934
walking_energy_cost = 28.16352
train_energy_cost = 56.327
car_energy_cost = 643.738

# https://nacto.org/shared-micromobility-2020-2021/
# IN THOUSANDS
shared_ridership_total = {2010: 321, 2011: 2400, 2012: 4500, 2013: 13000, 2014: 18000, 2015:22000, 2016:28000, 2017:35000, 2018: 45000, 2019: 49000, 2020: 28000, 2021: 48000}

# constants about human calories put into transport (we want healthiness!) (measures in calories/mile)
# also use disclaimer!!!!! because these constants are super sketch

# https://www.focus.de/gesundheit/praxistipps/gelber-bluetenstaub-dicke-luft-problem-fuer-allergiker-folgen-des-klimawandels_id_8851576.html
ebike_calories_burned_per_mile = 1/(trip_avg_official_speed * (1/300))

# https://www.livestrong.com/article/135430-calories-burned-biking-one-mile/
bike_calories_burned_per_mile = 55

# https://www.nerdfitness.com/blog/walking/
walking_calories_burned_per_mile = 100

# assuming that the other modes of transport are 0
car_calories_burned_per_mile = 0
public_transit_calories_burned_per_mile = 0


# actual constants

km_to_mile_multiplier = 0.62137
mile_to_km_multiplier = 1.60934
random_seed = 422

# format

date_format = "%Y-%m-%d %H:%M:%S"

# https://thenextweb.com/news/norwegian-ebike-owners-ride-4x-as-much-after-buying-their-bikes
# norway: assumption that norway is comparable to the US in terms of avg distance miles traveled
avg_miles_covered_per_day_by_ebike_owners = 5.2

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

    
