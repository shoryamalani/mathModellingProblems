data_folder = "data/"
import os
import numpy
import csv
def getWeatherData(location):
    # return the csv file for the location
    folder = "weather/"
    with open(data_folder + folder + location + ".csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        return list(reader)

def createLocationDataFolder(location):
    folder = "output/" + location + "/"
    if not os.path.exists(data_folder + folder):
        os.makedirs(data_folder + folder)



if __name__ == "__main__":
    print(getWeatherData("Georgia"))
