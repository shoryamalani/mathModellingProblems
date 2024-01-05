import dataWorker
class Fielder:
    def __init__(self, name, year):
        self.name = name
        self.year = year
    def __init__(self,player_id,year):
        self.player_id = player_id
        self.year = year
        self.data = dataWorker.get_player_by_id(player_id)
        self.name = self.data['stats']['first_name'] + " " + self.data['stats']['last_name']
        self.bulk_data = dataWorker.get_fielder_by_name(self.name,year)
    def get_def(self):
        return self.bulk_data['PO']/self.bulk_data['Ch']

