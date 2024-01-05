import os
import requests
import json
import mlbstatsapi
import pandas as pd
import constants
import statsapi
mlb = mlbstatsapi.Mlb()
# get umpire data













def get_memoized_player_data(player_id):
    if player_id + ".json" in os.listdir(constants.specific_player_data_path):
        with open(os.path.join(constants.specific_player_data_path,player_id+".json"),'r') as f:
            return json.load(f)
# get player data
def get_player_data_by_name(player_name):
    with open(os.path.join(constants.all_player_data_path,"all_players.json"),'r') as f:
        cur_players = json.load(f)
        if player_name in cur_players:
            id =  cur_players[player_name]
            return get_memoized_player_data(id)
    player_gen = statsapi.lookup_player(player_name)
    if len(player_gen) == 0:
        return None
    player_id = str(player_gen[0]['id'])
    
    player_data = statsapi.player_stat_data(player_id,group='[hitting,pitching,fielding]',type='[career,season,yearByYear]')
    final_data = {
        'general':player_gen[0],
        'stats':player_data
    }
    with open(os.path.join(constants.specific_player_data_path,player_id+".json"),'w') as f:
        json.dump(final_data,f)
    with open(os.path.join(constants.all_player_data_path,"all_players.json"),'r+') as f:
        cur_players = json.load(f)
        cur_players[player_name] = player_id
        f.seek(0)
        f.flush()
        f.write(json.dumps(cur_players))
    return final_data

def get_player_by_id(player_id):
    player_id = str(int(player_id))
    if player_id + ".json" in os.listdir(constants.specific_player_data_path):
        with open(os.path.join(constants.specific_player_data_path,player_id+".json"),'r') as f:
            return json.load(f)

    player_data = statsapi.player_stat_data(player_id,group='[hitting,pitching,fielding]',type='[career,season,yearByYear]')
    print(player_data)
    player_gen = statsapi.lookup_player(player_data['first_name'] + " " + player_data['last_name'])
    if len(player_gen) == 0:
        print("no data for player id: " + player_id)
        player_gen = [{}]
    final_data = {
        'general':player_gen[0],
        'stats':player_data
    }
    with open(os.path.join(constants.all_player_data_path,"all_players.json"),'r+') as f:
        cur_players = json.load(f)
        cur_players[player_data['first_name'] + " " + player_data['last_name']] = player_id
        f.seek(0)
        f.flush()
        f.write(json.dumps(cur_players))
    with open(os.path.join(constants.specific_player_data_path,player_id+".json"),'w') as f:
        json.dump(final_data,f)
    return final_data

def get_player_bulk_pitch_data_by_name(player_name,year):
    fpath = os.path.join(constants.pitching_data_path,str('bulk_'+str(year)+ ".csv"))
    data = pd.read_csv(fpath)
    for index,row in data.iterrows():
        # take away accents from both
        row["Name"] =  row["Name"].encode('ascii', 'ignore').decode('ascii')
        row["Name"] = row["Name"].strip("*")
        row["Name"] = row["Name"].replace("#","")
        row["Name"] = row["Name"].replace("Jr.","")
        row["Name"] = row["Name"].replace("á","a")
        row["Name"] = row["Name"].replace("é","e")
        row["Name"] = row["Name"].strip()
        player_name = player_name.encode('ascii', 'ignore').decode('ascii')
        if row["Name"] == player_name:
            return row
    return None

def get_fielder_by_name(name,year):
    fpath = os.path.join(constants.fielding_data_path,str('bulk_'+str(year)+ ".csv"))
    data = pd.read_csv(fpath)
    for index,row in data.iterrows():
        # take away accents from both
        # row["Name"] =  row["Name"].encode('ascii', 'ignore').decode('ascii')
        row["Name"] = row["Name"].replace("*","")
        row["Name"] = row["Name"].replace("#","")
        row["Name"] = row["Name"].replace("Jr.","")
        row["Name"] = row["Name"].replace("á","a")
        row["Name"] = row["Name"].replace("é","e")
        row["Name"] = row["Name"].strip()
        name = name.replace("Jr.", "")
        name = name.strip()
        if row["Name"] == name:
            return row
    return None
def get_specific_player_bulk_pitch_data_by_name(player_name,year):
    fpath = os.path.join(constants.pitching_data_path,str('specific_'+str(year)+ ".csv"))
    data = pd.read_csv(fpath)
    for index,row in data.iterrows():
        # take away accents from both
        row["Name"] =  row["Name"].encode('ascii', 'ignore').decode('ascii')
        row["Name"] = row["Name"].strip("*")
        row["Name"] = row["Name"].replace("#","")
        row["Name"] = row["Name"].replace("Jr.","")
        row["Name"] = row["Name"].replace("á","a")
        row["Name"] = row["Name"].replace("é","e")
        row["Name"] = row["Name"].strip()
        player_name = player_name.encode('ascii', 'ignore').decode('ascii')
        if row["Name"] == player_name:
            return row
    return None

def get_bulk_batter_data_by_name(name,year):
    fpath = os.path.join(constants.batting_data_path,str('bulk_'+str(year)+ ".csv"))
    data = pd.read_csv(fpath)
    for index,row in data.iterrows():
        # take away accents from both
        # row["Name"] =  row["Name"].encode('ascii', 'ignore').decode('ascii')
        row["Name"] = row["Name"].strip("*")
        row["Name"] = row["Name"].replace("#","")
        row["Name"] = row["Name"].replace("Jr.","")
        row["Name"] = row["Name"].replace("á","a")
        row["Name"] = row["Name"].replace("é","e")
        row["Name"] = row["Name"].replace("II","")
        row["Name"] = row["Name"].strip()
        name = name.replace("Jr.", "")
        name = name.replace("II", "")
        name = name.strip()
        # name = name.encode('ascii', 'ignore').decode('ascii')
        if row["Name"] == name:
            return row
        
    
    return None
    

    



if __name__ == "__main__":
    # print(get_player_data_by_name("David Villar"))
    print(get_player_by_id("606132"))
    




