
import dataWorker
class Pitcher:
    name = None
    def __init__(self, name, year,team_name):
        try:
            int(name)
            return self(player_id=name,year=year)
        except:
            self.name = name
            self.year = year
        self.data = dataWorker.get_player_data_by_name(name)
        self.bulk_data = dataWorker.get_player_bulk_pitch_data_by_name(name,year)
        self.specific_data = dataWorker.get_specific_player_bulk_pitch_data_by_name(name,year)




        
    def __init__(self,player_id,year,team_name):
        self.player_id = player_id
        self.year = year
        self.data = dataWorker.get_player_by_id(player_id)
        if 'fullName' in self.data['general']:
            self.name = self.data['general']['fullName']
        else:
            self.name = self.data['general']['firstName'] + " " + self.data['general']['lastName']
        self.bulk_data = dataWorker.get_player_bulk_pitch_data_by_name(self.name,year)
        self.specific_data = dataWorker.get_specific_player_bulk_pitch_data_by_name(self.name,year)
    def getOBP(self):
        for year in self.data['stats']['stats']:
            if year['type'] == "yearByYear":
                if year['season'] == self.year and 'pitching' == year['group']:
                    return year['stats']['obp']
        for career in self.data['stats']['stats']:
            if career['type'] == 'career' and 'pitching' == career['group']:
                return career['stats']['obp']
    def get_fielding_strength(self):
        for year in self.data['stats']['stats']:
            if year['type'] == "yearByYear":
                if year['season'] == self.year and 'pitching' == year['group']:
                    return career['stats']['outs']/career['stats']['numberOfPitches']
        for career in self.data['stats']['stats']:
            if career['type'] == 'career' and 'pitching' == career['group']:
                return career['stats']['outs']/career['stats']['numberOfPitches']
    def get_strike_rate(self):
        return float(self.bulk_data['Str%'].replace("%",""))/100
    def get_foul_rate(self):
        return ((self.bulk_data['Str'] * float(self.bulk_data['F/Str'] .replace("%",""))/100)/self.bulk_data['PA'])/self.bulk_data['Pit/PA']
    def get_ball_rate(self):
        return self.specific_data['BB']/self.bulk_data['PA']
    def get_def(self):
        return 0.23