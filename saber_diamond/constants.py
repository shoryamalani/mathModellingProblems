import APIKEYS
import json
stats_api_base_url = "https://mlb-data.p.rapidapi.com/"
headers = {
    'x-rapidapi-key': APIKEYS.XRapidAPIKey,
    'x-rapidapi-host': "mlb-data.p.rapidapi.com"
    }
specific_player_data_path = "data/player_data/specific_player_data/"

all_player_data_path = "data/player_data/"

all_game_data_path = "data/game_data/"

fielding_data_path = "data/player_data/fielding/"
pitching_data_path = "data/player_data/pitching/"
batting_data_path = "data/player_data/batting/"

format_of_game_date = "%m/%d/%Y"

with open("data/averages.json",'r') as f:
    averages = json.load(f)

margin_fault_x = 0.0

margin_fault_z = 0.0