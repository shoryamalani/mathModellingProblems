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