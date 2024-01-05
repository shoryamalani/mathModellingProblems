import weather_data
import datetime
import random
import numpy as np
diseases = {
"Varroa": {
    "rateChange": 5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"Mites": {
    "rateChange": 0.5,
    "changeType": "mortalityRate",
    "prevalence": 0.5,
},
"Africanized": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"Chalkbrood": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"American Foulbrood": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"European Foulbrood": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"Nosema": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"Small Hive Beetle": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
},
"Carpenter Bee": {
    "rateChange": 0.5,
    "changeType": "eggLayingRate",
    "prevalence": 0.5,
}
}

disease_real_prevelance = weather_data.compile_disease_data()

class Beehive:
    def __init__(self, name, location, queen, population, date,amountOfPollenPerSquareMeter,state):
        self.name = name
        self.location = state
        self.get_weather()
        self.iqueen = queen
        self.ipopulation = population
        self.population = population
        self.idate = date
        self.date = date
        self.percentOfEggToAdult = 0.5
        self.eggLayingRate = 0.5
        self.mortalityRate = 0.5
        self.amountOfPollenPerSquareMeter = amountOfPollenPerSquareMeter
        self.currentDiseases = []
        self.state = state
        self.history = {}
    def get_weather(self):
        # get weather data from weather_data.py
        # return weather data
        self.weather_data = weather_data.get_weather_data(self.location)
        return self.weather_data

    def __str__(self):
        return f"{self.name} {self.location} {self.currentDiseases} {self.population} {self.date}"

    def __repr__(self):
        return f"{self.name} {self.location} {self.currentDiseases} {self.population} {self.date}"
    
    def run_time_segment(self):
        currentMortalityRate = self.mortalityRate
        curQuarter = 0
        if self.date.month < 13:
            curQuarter = 3
        elif self.date.month < 10:
            curQuarter = 2
        elif self.date.month < 7:
            curQuarter = 1
        else:
            curQuarter = 0
        # calculating getting diseases
        for disease,value in disease_real_prevelance.items():
            random.randint(0,10000)
            if self.state in value:
                chance = (value[self.state][curQuarter] * 100)/(91.25*12) 
                # 91.25 is the average number of days in a quarter and 12 is the number of days per segment
                if random.randint(0,10000) < chance:
                    self.currentDiseases.append(disease)
                    # self.mortalityRate += diseases[disease]["rateChange"]
            else:
                chance = value["United States"][curQuarter] * 100//(91.25*12) 
                if random.randint(0,10000) < chance:
                    self.currentDiseases.append(disease)
                    # self.mortalityRate += diseases[disease]["rateChange"]


        for disease in self.currentDiseases:
            if disease["changeType"] == "mortalityRate":
                currentMortalityRate *= disease["rateChange"]
            elif disease["changeType"] == "eggLayingRate":
                self.eggLayingRate *= disease["rateChange"]
        #random multiplier for mortality rate and egg laying rate
        
        currentMortalityRateRand = np.random.normal(1,0.25)
        currentEggLayingRateRand = np.random.normal(1,0.25)
        currentEggLayingRate = self.eggLayingRate
        currentPopulation = self.population
        currentPopulation = currentPopulation - (currentPopulation * currentMortalityRate * currentMortalityRateRand) + (currentPopulation * currentEggLayingRate *currentEggLayingRateRand)
        self.population = currentPopulation
        self.date = self.date + datetime.timedelta(days=12)
        self.history[self.date] = self.population
        return self.population


# def getLocationData(location):

if __name__ == "__main__":
    start_date = datetime.datetime(2020, 1, 1)
    beehive = Beehive("Beehive 1", "England", "Queen 1", 100, start_date, 0.5,"Alabama")
    beehive_2 = Beehive("Beehive 2", "England", "Queen 1", 100, start_date, 0.5,"Alabama")
    print(beehive)
    print(beehive_2)

    beehive.run_time_segment()
    beehive.run_time_segment()
    beehive.run_time_segment()
    beehive.run_time_segment()
    beehive_2.run_time_segment()
    beehive_2.run_time_segment()
    beehive_2.run_time_segment()
    beehive_2.run_time_segment()
    

    print(beehive)
    print(beehive_2)