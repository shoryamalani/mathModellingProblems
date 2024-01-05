# create a class that creates a x,y map of some class which allows us to calculate change over time
# the class should be able to snapshot the current state of the map and then calculate the change
# it should be able to create graph images of state and change at any time


# all distance is in meters
# all time is in day
# all speed is in meters/day
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import random
import data_worker
import math
import uuid
from PIL import Image
import datetime
import multiprocessing
import pandas
totalMap = None
sRelease = None
sGermination = None
sWeatherDirection = None
population = {
    
}
class ConstantGenerator:
    location = None
    month = None
    day = None
    locationWeatherData = {}
    def __init__(self, location,month, day):
        self.location = location
        self.createLocationData(location)
        self.month = month
        self.day = day
        reader = data_worker.getWeatherData(location) # returns csv reader
        for row in reader:
            self.locationWeatherData[row[0]] = row[1:]
    
    def createLocationData(self, location):
        data_worker.createLocationDataFolder(location)
    def addDay(self):
        day = datetime.datetime(2019, self.month, self.day)
        day += datetime.timedelta(days=1)
        self.month = day.month
        self.day = day.day

    def getPercentChanceOfGermination(self):
        wData = self.getWeatherDataDay(self.month,self.day)
        # get time of day and time of night
        if wData['tempC'] < 5 and wData["tempC"] > 35:
            return 0
        hoursDay = wData['sunrise'] # 05:40 AM
        hoursNight = wData['sunset']
        hoursDay = datetime.datetime.strptime(hoursDay, '%I:%M %p')
        hoursNight = datetime.datetime.strptime(hoursNight, '%I:%M %p')
        # get deltatime
        delta = hoursNight - hoursDay
        # get percent of day
        percentDay = delta.total_seconds() / 86400
        percentNight = 1 - percentDay
        percent = percentDay * self.computeDayGerminationPercent(wData['tempC']) + percentNight * self.computeNightGerminationPercent(wData['tempC'])
        
        return percent
            

    def computeDayGerminationPercent(self, tempC ):
        return (80.8269 * math.e ** (-0.00509821 *math.pow(tempC-16.9705,2)))/100
    
    def computeNightGerminationPercent(self, tempC):
        return (30.152 * math.e ** (-0.0149758 *math.pow(tempC-16.75,2)))/100


    def getWeatherDataDay(self,month,day):
        day = datetime.datetime(2019, month, day)
        dayString = day.strftime("%Y-%m-%d")
        # maxtempC	mintempC	totalSnow_cm	sunHour	uvIndex	moon_illumination	moonrise	moonset	sunrise	sunset	DewPointC	FeelsLikeC	HeatIndexC	WindChillC	WindGustKmph	cloudcover	humidity	precipMM	pressure	tempC	visibility	winddirDegree	windspeedKmph	location
        values = self.locationWeatherData[dayString]
        
        return  {
            "maxtempC": values[0],
            "mintempC": values[1],
            "totalSnow_cm": values[2],
            "sunHour": values[3],
            "uvIndex": values[4],
            "moon_illumination": values[5],
            "moonrise": values[6],
            "moonset": values[7],
            "sunrise": values[8],
            "sunset": values[9],
            "DewPointC": values[10],
            "FeelsLikeC": values[11],
            "HeatIndexC": values[12],
            "WindChillC": values[13],
            "WindGustKmph": int(values[14]),
            "cloudcover": values[15],
            "humidity": values[16],
            "precipMM": values[17],
            "pressure": values[18],
            "tempC": float(values[19]),
            "visibility": values[20],
            "winddirDegree": int(values[21]),
            "windspeedKmph": int(values[22]),
            "location": values[23]
        }


    def calculateProportionOfSeedsToRelease(self):
        windSpeed = self.convertKmphToMetersPerSecond(self.getWeatherDataDay(self.month,self.day)['windspeedKmph'])/5
        # logistic function
        proportion = 1/(1+np.exp(-windSpeed)) 
        proportion = (100 -151.147 * math.e ** (-1.52489 * windSpeed))/(100)
        return proportion


    def convertKmphToMetersPerSecond(self, kmph):
        return kmph * 1000 / 3600
    
    def getWeatherDirection(self):
        d = self.getWeatherDataDay(self.month,self.day)
        deg = int(d['winddirDegree'])
        # convert to radians
        rad = deg * math.pi/180
        return rad

    def getWindSpeedMetersPerSecond(self):
        d = self.getWeatherDataDay(self.month,self.day)
        return self.convertKmphToMetersPerSecond(d['windspeedKmph'])

    def getHumidity(self):
        d = self.getWeatherDataDay(self.month,self.day)
        return float(d['humidity'])

    def calculateDistanceSeedTravels(self):
        # return 1
        d = self.getWeatherDataDay(self.month,self.day)
        # if random.random() > 0.90:
        # windSpeed = self.convertKmphToMetersPerSecond(d['WindGustKmph']) 
        # else:
        windSpeed = self.convertKmphToMetersPerSecond(d['windspeedKmph'])
        # make a skewed distribution
        # 0 to 1
        # val = random.(0,1)
        # windSpeed = 2
        rHeight = max(random.normalvariate(0.3,0.05),0.01)
        fallSpeed = 0.3
        if(float(d['humidity']) < 80 ):
            fallSpeed = 0.3 
        elif (float(d['humidity']) > 80 and float(d['humidity']) < 90  ):
            fallSpeed = 0.4
        else:
            fallSpeed = 0.7
        a = math.log((rHeight*windSpeed)/fallSpeed,math.e)
        # # print(a)
        # for a in range(1000):
        distance = np.random.lognormal(a,.25*windSpeed)
        
        # # numpy show distribution
        # for i in range(1000):
        #     if distribution[i] == math.inf:
        #         distance = 100
        #         break
        # plt.hist(distribution, bins=100)

        
        # print(distance)
        # print(windSpeed)
        # if distance > 1:
        #     print(distance)

        return distance

random.seed(422)

class DifferentialMap:
    xyMap = None

    def __init__(self, x, y):
        # x and y are the dimensions of the map
        # create a map of x,y
        self.x = x
        self.y = y
        self.xyMap = self.createBlankDimensionArray()
        for i in range(y):
            for j in range(x):
                self.xyMap[i][j] = PlantSpot(j, i)
        self.xyMap[75][25] = PlantSpot(75,25,1)

    def calculateChange(self):
        # for performance reasons, we will calculate the change on each plant spot
        global sRelease
        global sGermination
        global sWeatherDirection
        sRelease = cGen.calculateProportionOfSeedsToRelease()
        sGermination = cGen.getPercentChanceOfGermination()
        sWeatherDirection = cGen.getWeatherDirection()
        curSeedsToMove = {

        }
        totalToMove = 0
        for y in range(len(self.xyMap)):
            for x in range(len(self.xyMap[y])):
                self.xyMap[y][x].calculateChangeOnSelf()
                seedsToMove = self.xyMap[y][x].calculateChangeOnOthers()
                if seedsToMove == 0:
                    continue
                curSeedsToMove[(x,y)] = seedsToMove
                totalToMove += seedsToMove
        # calculate transformations for all seeds at once with multiprocessing
        # open 10 processes
        # print(curSeedsToMove)
        queue = multiprocessing.Queue()
        totals = []
        totalThreads = 10
        if totalToMove > 100000000:
            totalToMove = 100000000
        if totalToMove == 0:
            return
        if totalToMove/1000 < 10:
            totalThreads = max(math.floor(totalToMove/1000),1)
        for a in range(totalThreads):
            totals.append(math.floor(totalToMove/totalThreads))
        totals[totalThreads-1] += totalToMove % totalThreads
        processes = []
        print(totals)
        for a in range(totalThreads):
            p = multiprocessing.Process(target=self.calculateSeedMovement, args=(totals[a],cGen.getWindSpeedMetersPerSecond(),cGen.getHumidity(),sWeatherDirection,queue))
            processes.append(p)
            p.start()
            
        
        # for p in processes:
        #     p.join()
        transformations = []
        for a in range(totalThreads):
            transformations += queue.get()
        for p in processes:
            p.terminate()
        # print(transformations)
        # go through each of the curSeedsToMove and move them using the transformations
        for key in curSeedsToMove:
            for i in range(curSeedsToMove[key]):
                if len(transformations) == 0:
                    break
                startTransform = transformations.pop()
                x = key[0] + startTransform[0]
                y = key[1] + startTransform[1]
                if x < 0 or y < 0:
                    continue
                if x > 149 or y > 149:
                    continue 
                # print(x,y)
                totalMap.addSeedToLocation(x,y)

            



        
        # for y in range(len(self.xyMap)):
        #     for x in range(len(self.xyMap[y])):
                
    def calculateSeedMovement(self, totalToMove,windSpeed,humidity,sWeatherDirection,queue): 
        transformations = []
        for _ in range(totalToMove):
                rHeight = max(random.normalvariate(0.3,0.05),0.01)
                fallSpeed = 0.3
                if(humidity < 80 ):
                    fallSpeed = 0.3 
                elif (humidity > 80 and humidity < 90  ):
                    fallSpeed = 0.4
                else:
                    fallSpeed = 0.7
                a = math.log((rHeight*windSpeed)/fallSpeed,math.e)
                # # print(a)
                # for a in range(1000):
                distance = np.random.lognormal(a,.25*windSpeed)
                d = random.normalvariate(sWeatherDirection,.36) % (2*math.pi)
                x = distance * math.cos(d)
                y = distance * math.sin(d)
                x = round(x)
                y = round(y) 
                
                transformations.append((x,y))

        queue.put(transformations)
    def setImpact(self, x, y, impact):
        self.xyMap[y, x].addImpact(impact)

    def snapshot(self,m, changeOrCurrent):
        # create pixel map
        # red,orange,yellow,green is 0 to max
        # where red is -max, orange is -max/2, yellow is 0, green is max/2, blue is max
        # essentially create a pixel based on value
        # if changeOrCurrent is true then return current change
            # create a 2d array of colors
            # convert 2d array of colors to image
            # finalValues = self.createBlankDimensionArray()
            # for y in range(len(self.xyMap)):
            #     for x in range(len(self.xyMap[y])):
            #         finalValues[y][x] = [self.xyMap[y][x].getCurrentValueOfDandelions()]
        
        finalColors = self.createBlankDimensionArray()
        for y in range(len(self.xyMap)):
            for x in range(len(self.xyMap[y])):
                colorIntensity = int(min(len(self.xyMap[y][x].dandelions)/m,1) * 255)
                colorIntensityNewness = int(min(self.xyMap[y][x].getAverageAge()/45,1) * 255)
                colorIntensitySeeds = int(min(self.xyMap[y][x].getNumberOfDandelionSeeds()/50,1) * 255)
                finalColors[y][x] = [colorIntensitySeeds, colorIntensity, colorIntensityNewness]
        
        # make image from colors
        # this is not working for some reason
        img = Image.fromarray(np.array(finalColors, dtype=np.uint8), 'RGB')
        for x in range(25,125):
            img.putpixel((x,25),(255,0,0))
            img.putpixel((x,124),(255,0,0))
        for y in range(25,125):
            img.putpixel((25,y),(255,0,0))
            img.putpixel((124,y),(255,0,0))
        img = img.resize((800,800), Image.NEAREST)
        # add red border around middle 50%
        population[cGen.location].append(self.getPopulation())    
            
        print(population)
        
        img.save("data/"+"output/"+cGen.location+'/my'+str(cGen.month)+"-"+str(cGen.day)+'.png')
        # px.imshow(finalColors).show()

    def getPopulation(self):
        population = 0
        for y in range(25,125):
            for x in range(25,125):
                population += len(self.xyMap[y][x].dandelions)
        return population
        

    def createBlankDimensionArray(self):
        arr = []
        for a in range(self.x):
            arr.append([])
            for b in range(self.y):
                arr[a].append(None)
        return arr

    def addSeedToLocation(self, x, y):
        # print(x,y)
        self.xyMap[y][x].addSeed()
        # print(self.xyMap[y][x].numberOfDandelionSeeds)
    
    




class PlantSpot:
    def __init__(self, x, y,startAgedDandelions=0):
        self.dandelions = []
        self.dandelionsAdded = 0
        self.plants = []
        self.externalImpacts = []
        self.plantsPerSquareMeter = 0
        self.numberOfDandelionSeeds = 0
        self.x = x
        self.y = y
        for i in range(startAgedDandelions):
            self.dandelions.append(Dandelion(60))
            self.dandelionsAdded += 1

    def getAverageAge(self):
        age = 0
        for dandelion in self.dandelions:
            age += dandelion.daysAlive
        if len(self.dandelions) == 0:
            return 0
        return age/len(self.dandelions)
    def getNumberOfDandelionSeeds(self):
        seeds = self.numberOfDandelionSeeds
        return seeds
    

    
    def calculateChangeOnSelf(self):
        self.calculateSeedsIntoDandelions()

        # if(len(self.dandelions) != 0):
            # print(self.numberOfDandelionSeeds)
            # print(cGen.day, len(self.dandelions),self.x,self.y)
            # print(self.dandelions[0].daysAlive)
            

    def calculateChangeOnOthers(self):
        seedsToRemove = 0
        for dandelion in self.dandelions:
            seedsToRemove += dandelion.plusTime(sRelease)
            if dandelion.calculateDeath():
                self.dandelions.remove(dandelion)
        return seedsToRemove



    def getCurrentValueOfDandelions(self):
        pass

    def getCurrentChangeOfDandelions(self):
        pass

    def getCurrentChangeOfSeeds(self):
        pass

    def calculateSeedsIntoDandelions(self):
        seedsGrown = round(self.numberOfDandelionSeeds * sGermination)
        self.numberOfDandelionSeeds -= seedsGrown

        for i in range(seedsGrown):
            if(len(self.dandelions)> 8):
                break
            self.dandelions.append(Dandelion(0))
        pass

    def addSeed(self):
        self.numberOfDandelionSeeds += 1






class Plant:
    growthRate = 0
    impactCoefficient = 0
    impactRadius = 0


class Dandelion(Plant):
    

    def __init__(self):
        
        self.calculateNumberOfFlowers()
        self.calculateSeedsToGrow()
    
    def __init__(self, startAged=0):
        self.numberOfFlowers = 0
        self.daysAlive = 0
        self.seedsToGrow = 0 
        self.seedsGrown = 0
        self.seedsBlown = 0
        self.daysAlive = startAged
        self.growthDays = 8*7 + random.normalvariate(3.5,1) * 7
        self.calculateNumberOfFlowers()
        self.calculateSeedsToGrow()
        if (startAged != 0):
            self.growthDays = 0
            self.seedsGrown = self.seedsToGrow * self.numberOfFlowers

        
        
    def calculateSeedsToGrow(self):
        # mean 224 seeds per flower
        # deviation 54 seeds per flower
        self.seedsToGrow = round(random.gauss(224,54)) * self.numberOfFlowers

    def calculateSeedsToGrowPerDay(self):
        if self.daysAlive >= self.growthDays:
            self.seedsGrown += self.seedsToGrow * self.numberOfFlowers
            self.seedsToGrow = 0
        pass

    def calculateNumberOfFlowers(self):
        self.numberOfFlowers = round(random.gauss(10,2))
        # log normal distribution
        # self.numberOfFlowers = np.random.lognormal(3, 1)
        
    def plusTime(self, proportionOfSeedsReleased):
        seedsToRemove = math.floor(self.seedsGrown * proportionOfSeedsReleased)
        # if seedsToRemove > 0:
        #     print(seedsToRemove)
        self.seedsGrown -= seedsToRemove
        self.seedsBlown += seedsToRemove
        self.calculateSeedsToGrowPerDay()
        self.daysAlive += 1
        return seedsToRemove

    
    def calculateDeath(self):
        if self.seedsBlown > self.seedsToGrow:
            return True
    


    
if __name__ == "__main__":
    totalMap = DifferentialMap(150,150)
    cGen = ConstantGenerator("Arizona", 1,1)
    population[cGen.location] = []
    for i in range(364):
        totalMap.calculateChange()
        cGen.addDay()
        totalMap.snapshot(10, False)
    
    # make df out of population with days as x and population as y and location as color and label
    # make a line graph out of it

    # move to csv
    df = pandas.DataFrame(population)
    df.to_csv("data/output/"+cGen.location+"/population.csv")


    
    
