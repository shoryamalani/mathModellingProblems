#monte_carlo_sim.py

from random import random
import matplotlib.pyplot as plt
import os

OBP = 0.317
players = 27
games_per_season = 2430
seasons = 50000
def monte_carlo_sim_perfect_game(obp,players):
    for _ in range(players):
        if random() < obp:
            return False
    return True

if __name__ == '__main__':
    perfect_games = 0
    for i in range(seasons):
        if i % 100 == 0:
            print(i)
            print(perfect_games)
        for _ in range(games_per_season):
            if monte_carlo_sim_perfect_game(OBP,players):
                perfect_games += 1
    print(perfect_games)

