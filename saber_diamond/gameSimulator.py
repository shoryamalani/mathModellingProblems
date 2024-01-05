import pandas as pd
import numpy as np
import os
import datetime
import random
from multiprocessing import Pool

import constants

from pitcher import Pitcher
from batter import Batter
from fielder import Fielder

test_vals = []


class gameFrame:
    def __init__(self,pitcher,batter,bases,outs,innings,home_score,away_score,strikes,balls,cur_team,fielders,home_team,away_team,home_batting_order,away_batting_order,year):
        self.pitcher = pitcher
        self.batter = batter
        self.bases = bases
        self.outs = outs
        self.innings = innings
        self.home_score = home_score
        self.away_score = away_score
        self.strikes = strikes
        self.balls = balls
        self.cur_team = cur_team
        self.fielders = fielders
        self.home_team = home_team
        self.away_team = away_team
        self.home_batting_order = home_batting_order
        self.away_batting_order = away_batting_order
        self.year  = year
    def get_pitcher_batter_interaction(self):
        pitcherOBP = float(self.pitcher.getOBP())
        batterOBP = float(self.batter.getOBP())
        average = constants.averages['obpA']['batting']['2022']
        # val = ((pitcherOBP*batterOBP)/(average))/((pitcherOBP*batterOBP)/(average)+((1-batterOBP)*((1-pitcherOBP)/(1-average))))
        val = (pitcherOBP*batterOBP *(1-average))/((pitcherOBP*batterOBP)-(pitcherOBP*average)-(batterOBP*average)+(average))
        return val

    def calculate_fielding_strength(self):
        # currently just using pitcher historical data
        self.pitcher.get_fielding_strength()

    def calculate_percentage_outcomes(self):
        
        obp = self.get_pitcher_batter_interaction() # percent change the ball is in play
        babip = self.batter.getBabip() # chances the ball goes in play
        percent_chances = {
            "ball":self.pitcher.get_ball_rate(),
            'foul': self.pitcher.get_foul_rate(),
            "strike": self.pitcher.get_strike_rate()-self.pitcher.get_foul_rate(),
            "hit_in_play":babip,
        }
        return percent_chances
    def get_hit_type_chances(self):
        return self.batter.get_hit_chances()
    def walk(self):
        forced_move = True
        cur_base = 0
        temp_base_man = None
        last_batter = self.batter
        while forced_move:
            if self.bases[cur_base] != None:
                temp_base_man = self.bases[cur_base]
                self.bases[cur_base] = last_batter
                last_batter = temp_base_man
                cur_base+=1
                if cur_base == 2:
                    self.score()
                    return None
            else:
                self.bases[cur_base] = last_batter
                forced_move = False



    def hit(self,key):
        key_vals = {
            "single" : 1,
            "double": 2,
            "triple": 3,
            "HR": 4,
        }
        next_player = self.batter
        for _ in range(key_vals[key]):
            if self.bases[2] != None:
                self.score()
            self.bases.insert(0,next_player)
            self.bases.pop()
            next_player = None
        
    def score(self):
        if self.cur_team == self.home_team:
            self.home_score+=1
        else:
            self.away_score+=1

    def get_new_batter(self):
        if self.batter.get_player_id() in self.get_cur_team_batting_order():
            self.batter = Batter(self.get_cur_team_batting_order()[(self.get_cur_team_batting_order().index(self.batter.get_player_id()) +1 )% 9],self.year,self.cur_team)
        else:
            self.batter = Batter(random.choice(self.get_cur_team_batting_order()),self.year,self.cur_team)
        # return None
    def get_cur_team_batting_order(self):
        if self.cur_team == self.home_team:
            return self.home_batting_order
        else:
            return self.away_batting_order
    def strikeout(self):
        self.get_new_batter()
        self.outs +=1

    def do(self,event):
        if event == "ball":
            if self.balls == 3:
                event = "walk"
            else:
                self.balls+=1
        if event == "strike":
            if self.strikes == 2:
                event = "strikeout"
            else:
                self.strikes +=1
        if event == "hit_by_pitch":
            event = 'walk'
        if event == "walk":
            self.walk()
            self.get_new_batter()
        if event == "strikeout":
            self.strikeout()
            self.get_new_batter()
        if event == 'foul':
            if self.strikes < 2:
                self.strikes +=1
        if event == "hit_in_play":
            hit_types = self.get_hit_type_chances()
            cum_sum = 0
            rng = random.random()
            for key,val in hit_types.items():
                cum_sum +=val
                if rng < cum_sum:
                    self.hit(key)
                    rng = random.random()
                    defen = self.get_fielder_catch()
                    self.get_new_batter()
                    if defen > rng:
                        self.out()
                    break
    def out(self):
        tot = 0
        for bas in self.bases:
            if bas != None:
                tot +=1
        val = random.randint(0,tot)
        tot = 0
        i = 0
        while i < 2:
            if bas != None:
                tot +=1
            if tot == val:
                self.bases[i] = None
            i+=1


    def get_fielder_catch(self):
        total = 0
        for fielder in self.fielders:
            total += fielder.get_def()
        return total/9



def calculate_game_frame(game_frame):
    # things needed to calculate game frame
    # calculate fielding strength
    rng = random.random()
    # calculate the chances the ball is hit
    # This only calculates the chance that the person moves to the next base, it could be a walk
    # walk could be calcualted using information from pitcher statsapi or from sabermetrics @(LATER)
    percents = game_frame.calculate_percentage_outcomes()
    cur_tot = 0
    for key,val in percents.items():
        cur_tot +=val
        if cur_tot > rng:
            test_vals.append(key)
            game_frame.do(key)
            break
    
    


            
        
    # calculate the chances that the pitch is a ball, strike, or foul and update strike and ball count

    

    
def get_batting_order(df):
    home_batting_order = df[df["inning_topbot"]=="Bot"]
    away_batting_order = df[df["inning_topbot"]=="Top"]
    home_order = []
    for index,row in home_batting_order.iterrows():
        batter = row['batter']
        if home_order == []:
            home_order.append(batter)
        if batter == home_order[0] and batter != home_order[-1]:
            break
        if batter != home_order[-1]:
            home_order.append(batter)
    away_order = []
    for index,row in away_batting_order.iterrows():
        batter = row['batter']
        if away_order == []:
            away_order.append(batter)
        if batter == away_order[0] and batter != away_order[-1]:
            break
        if batter != away_order[-1]:
            away_order.append(batter)

    return home_order,away_order
    
def find_fault_ball(row):
    cur_call = row.description
    ball = True
    if (abs(row.plate_x)<(0.708+0.12-constants.margin_fault_x)) and ((row.plate_z < row.sz_top + 0.12 - constants.margin_fault_z) and (row.plate_z > row.sz_bot - 0.12 + constants.margin_fault_z)): # should be a strike
        ball = False
    if not ball:
        return True
    return False
    
def find_fault_called_strikes(row):
    strike = True
    if not (abs(row.plate_x) < 0.708+ 0.12 + constants.margin_fault_x):
        strike = False
    if (row.plate_z> row.sz_top + 0.12 + constants.margin_fault_x) or (row.plate_z< row.sz_bot - 0.12 - constants.margin_fault_z):
        strike = False
    if not strike:
        return True
    return False

def game_follower(a,csv_name="NYY_at_MILK.csv"):
    df = pd.read_csv(os.path.join(constants.all_game_data_path,csv_name))
    # get batting order from all the rows to init
    scores = []
    home_order,away_order = get_batting_order(df)
    e_num = 0
    for index,row in df.iterrows():
        error = False
        if row.description == "ball" or row.description == 'blocked_ball':
            if find_fault_ball(row):
                error = True
                e_num +=1
        elif row.description == 'called_strike':
            if find_fault_called_strikes(row):
                error = True
                e_num+=1
        if error == True:
            pitcher_id = row.pitcher
            batter_id = row.batter
            game_date = datetime.datetime.strptime(row.game_date,constants.format_of_game_date)
            pitch_team = row.home_team
            bat_team = row.away_team
            if row.inning_topbot == "Top":
                pitch_team = row.away_team
                bat_team = row.home_team
            pitcher = Pitcher(pitcher_id,game_date.year,pitch_team)
            batter = Batter(batter_id,game_date.year,bat_team)
            bases = [Batter(row.on_1b,game_date.year,bat_team) if str(row.on_1b).strip() != "nan" else None,Batter(row.on_2b,game_date.year,bat_team) if str(row.on_2b).strip() != "nan" else None,Batter(row.on_3b,game_date.year,bat_team) if str(row.on_3b).strip() != "nan" else None]
            outs = row.outs_when_up
            strikes = row.strikes
            balls = row.balls
            inning = row.inning
            fielders = [pitcher,Fielder(row.fielder_2,game_date.year),Fielder(row.fielder_3,game_date.year),Fielder(row.fielder_4,game_date.year),Fielder(row.fielder_5,game_date.year),Fielder(row.fielder_6,game_date.year),Fielder(row.fielder_7,game_date.year),Fielder(row.fielder_8,game_date.year),Fielder(row.fielder_9,game_date.year)]
            cur_frame = gameFrame(pitcher,batter,bases,outs,inning,row.home_score,row.away_score,strikes,balls,pitch_team,fielders,row.home_team,row.away_team,home_order,away_order,game_date.year)
            while cur_frame.outs < 3:
                calculate_game_frame(cur_frame)
            scores.append([cur_frame.home_score,cur_frame.away_score])
    pd.DataFrame(scores).to_csv("export/"+str(a)+".csv")
    # print(e_num)
            
            




# multiprocess the game follower
def multiprocess_game_follower():
    pool = Pool(processes=20)
    # run game_follower 1000 times
    pool.map(game_follower,[a for a in range(1000)])
    pool.close()
    pool.join()

if __name__ == "__main__":
    multiprocess_game_follower()
    # game_follower(0)
    


        