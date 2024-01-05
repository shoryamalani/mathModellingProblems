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
