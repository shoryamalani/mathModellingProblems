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