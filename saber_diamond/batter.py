
import dataWorker
class Batter:
    name = None
    bulk_data = None
    def __init__(self, name, year,team_name):
        try:
            int(name)
            return self(player_id=name,year=year)
        except:
            self.name = name
            self.year = year
        self.data = dataWorker.get_player_data_by_name(self.name)
        self.bulk_data = dataWorker.get_bulk_batter_data_by_name(self.name,self.year)
        self.player_id = self.data['stats']['id']
    def __init__(self,player_id,year,team_name):
        self.player_id = player_id
        self.year = year
        self.data = dataWorker.get_player_by_id(player_id)
        if 'fullName' in self.data['general']:
            self.name = self.data['general']['fullName']
        else:
            self.name = self.data['stats']['first_name'] + " " + self.data['stats']['last_name']
        self.bulk_data = dataWorker.get_bulk_batter_data_by_name(self.name,self.year)
    
    def getOBP(self):
        for year in self.data['stats']['stats']:
            if year['type'] == "yearByYear":
                if year['season'] == self.year and 'hitting' == year['group']:
                    return year['stats']['obp']
        for career in self.data['stats']['stats']:
            if career['type'] == 'career' and 'hitting' == career['group']:
                return career['stats']['obp']
    def getBabip(self):
        for year in self.data['stats']['stats']:
            if year['type'] == "yearByYear":
                if year['season'] == self.year and 'hitting' == year['group']:
                    return year['stats']['babip']
        for career in self.data['stats']['stats']:
            if career['type'] == 'career' and 'hitting' == career['group']:
                return float(career['stats']['babip'])
    def get_hit_chances(self):
        percentages =  {
            "single": 1-((self.bulk_data['2B']+self.bulk_data['3B']+self.bulk_data['HR'])/(self.bulk_data["H"])),
            "double":self.bulk_data['2B']/self.bulk_data["H"],
            "triple":self.bulk_data['3B']/self.bulk_data['H'],
            "HR":self.bulk_data["HR"]/self.bulk_data["H"],
            "Outs": self.get_caught_percentage()
        }
        return percentages
    def get_player_id(self):
        return self.player_id
    def get_caught_percentage(self):
        for year in self.data['stats']['stats']:
            if year['type'] == "yearByYear":
                if year['season'] == self.year and 'hitting' == year['group']:
                    return year['stats']['babip']
        for career in self.data['stats']['stats']:
            if career['type'] == 'career' and 'hitting' == career['group']:
                return float(career['stats']['babip'])
    def get_walk_rate(self):
        try:
            return self.bulk_data['BB']/self.bulk_data['PA']
        except:
            return .05
    def get_foul_rate(self):
        try:
            return (self.bulk_data['AB']-self.bulk_data['H']-self.bulk_data["HBP"]-self.bulk_data["BB"])/self.bulk_data['AB']
        except:
            return .20
