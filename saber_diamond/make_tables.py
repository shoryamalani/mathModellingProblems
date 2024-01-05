import os
import pandas as pd
innings_score = [[0,0],[1,0],[1,0],[1,0],[2,0],[2,0],[2,1],[2,4],[4,4],[5,5],[6,6],[7,6]]
errors = [1,1,1,2,3,3,3,3,3,3,4,5,5,6,6,6,6,7,7,8,9,9,9,10,11,11]
all_scores = [[0,0] for x in range(len(errors))]
# average 1000 csv files
# get all column ones and average them
# get all column twos and average them
dfs = []
for i in range(1000):
    if str(i) + ".csv" not in os.listdir('export'):
        continue
    df = pd.read_csv(os.path.join('export',str(i)+ ".csv"))
    dfs.append(df)
print(pd.concat(dfs).groupby(level=0).mean().to_csv('export.csv'))
pd.Series(innings_score).to_csv('innings_score.csv')
    

    