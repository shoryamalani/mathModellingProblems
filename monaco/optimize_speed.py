from time import time
from numpy import true_divide
import pandas
import random
import itertools
MAXTIRE = [14,39,53]
POSSIBLE_TIRE_CONFIGS = []

for x in range(2,7):
    current_config = []
    for y in range(3):
        for _ in range(x):
            current_config.append(y)
    POSSIBLE_TIRE_CONFIGS.append(set(itertools.permutations(current_config,x)))
inter_configs = []
for config in POSSIBLE_TIRE_CONFIGS:
    inter_config = []
    for tires in config:
        if len(set(tires)) != 1:
            inter_config.append(tires)
    inter_configs.append(inter_config)
POSSIBLE_TIRE_CONFIGS = inter_configs
print(POSSIBLE_TIRE_CONFIGS)


def open_csv(file_name):
    df = pandas.read_csv(file_name)
    return df

def make_tires(df):
    tires = []
    for row in df:
        final_tire_values = []
        for value in df[row].values:
            try:
                if row=="Hard":
                    final_tire_values.append(int(value)+random.randint(0,25)/100)
                elif row=="Medium":
                    final_tire_values.append(int(value)+random.randint(0,75)/100)
                else:
                    final_tire_values.append(int(value)+random.randint(0,200)/100)
            except:
                pass
        tires.append(final_tire_values)
        print(final_tire_values)
    final_tires = []
    for tire in tires[1:]:
        current_val = 0
        current_tire = []
        for value in tire:
            current_val+= value
            current_tire.append(current_val)
        final_tires.append(current_tire)
    print(final_tires)
    return final_tires



def check_possible(permution):
    last_x = None
    for x in list(permution):
        # print(x)
        if last_x == None:
            last_x = x
            if x > 40:
                return False
        elif x - last_x > 40:
            return False
        else:
            last_x = x
    if 78-x> 40:
        return False
    return True

old_lowest = 100000

def find_best_situation(laps,pit_stops,tires):
    permutations = itertools.combinations([x+1 for x in range(laps-1)],pit_stops)
    # return permutations
    lowest = 100000
    final_permutations = []
    
    for permutation in permutations:
        if 35 in permutation:
            final_permutations.append(permutation)
    
    perm = None
    for permutation in final_permutations:
        if check_possible(permutation):
            x,y = try_all_tires(permutation,tires,laps,pit_stops)
            # if len(set(y)) >1:
            if x + (pit_stops*25) < lowest:
                lowest = x + (pit_stops*25)
                print(lowest)
                perm = permutation
                tire_config = y
                print(perm)
                print(tire_config)
    if lowest < old_lowest:
        print(lowest)
        print(perm)
        print(tire_config)
    # print(perm)
    # print(tire_config)
def try_all_tires(order,tires,laps,pit_stops):
    order = list(order)
    # order.append(35)
    order.append(78)
    least_time = 1000000
    final_tires = []
    try:
        for tire_config in POSSIBLE_TIRE_CONFIGS[pit_stops-1]:
            current_time = 0
            running_combo = True
            delta_laps = []
            x=0
            for lap in order:
                delta_laps.append(lap-x)
                x = lap
            # print(delta_laps)

            x = 0
            finished_combo = False
            while running_combo:
                if delta_laps[x] > MAXTIRE[tire_config[x]]:
                    running_combo = False
                else:
                    try:
                        current_time += tires[tire_config[x]][delta_laps[x]-1]
                    except:
                        current_time += 100000
                    x+=1
                    if x == len(delta_laps):
                        running_combo = False
                        finished_combo = True
            if current_time < least_time and finished_combo:
                least_time = current_time
                final_tires = tire_config
            # current_tires = tire_config[0]
            # for lap in delta_laps:
                # if lap < 
                # pass

            # while running_combo:
            if pit_stops -1 > len(POSSIBLE_TIRE_CONFIGS):
                return least_time,final_tires
        return least_time,final_tires
    except:
        return least_time,final_tires
    # for a in range(3):
    #     current_tires = []
    #     last_lap = 0
    #     current_time = 0
    #     current_tire = a
    #     current_tires.append(current_tire)
    #     for x in range(len(order)):
    #         tires_available = []
    #         for tire in range(3):
    #             if order[x]-last_lap < MAXTIRE[tire]:
    #                 tires_available.append(tire)
    #         least_amount = 1000000000
    #         tires_used = None
    #         for tire in tires_available:
    #             if tires[tire][order[x]-last_lap-1] < least_amount:
    #                 least_amount = tires[tire][order[x]-last_lap-1]
    #                 tires_used = tire
    #         current_time+= least_amount
    #         current_tires.append(tires_used)
    #         last_lap=order[x]
    #     if current_time < least_time:
    #         least_time = current_time
    #         current_time = 0
    #         final_tires = current_tires
    #     final_tires.pop()
    return least_time,final_tires
                
            
        

def make_schedule(tires,laps):
    current_tires = None
    timings = []
    for pit_stops in range(2,16): # number of pit stops
        timings.append(find_best_situation(laps,pit_stops,tires))


# def find_best_tire_switch(current_tires,laps_on_tire,laps,tires):
    

if __name__ == "__main__":
    laps=78
    # df = open_csv("AaronBalance.csv")
    df = open_csv("Monaco+Grand+Prix.csv")
    tires = make_tires(df)
    make_schedule(tires,laps)
# from time import time
# from numpy import true_divide
# import pandas
# import itertools
# MAXTIRE = [28,39,53]
# POSSIBLE_TIRE_CONFIGS = []

# for x in range(2,7):
#     current_config = []
#     for y in range(2):
#         for _ in range(x):
#             current_config.append(y)
#     POSSIBLE_TIRE_CONFIGS.append(set(itertools.permutations(current_config,x)))
# inter_configs = []
# for config in POSSIBLE_TIRE_CONFIGS:
#     inter_config = []
#     for tires in config:
#         if len(set(tires)) != 1:
#             inter_config.append(tires)
#     inter_configs.append(inter_config)
# POSSIBLE_TIRE_CONFIGS = inter_configs



# def open_csv(file_name):
#     df = pandas.read_csv(file_name)
#     return df

# def make_tires(df):
#     tires = []
#     for row in df:
#         final_tire_values = []
#         for value in df[row].values:
#             try:
#                 final_tire_values.append(int(value))
#             except:
#                 pass
#         tires.append(final_tire_values)
#     final_tires = []
#     for tire in tires[1:]:
#         current_val = 0
#         current_tire = []
#         for value in tire:
#             current_val+= value
#             current_tire.append(current_val)
#         final_tires.append(current_tire)
#     return final_tires



# def check_possible(permution):
#     last_x = None
#     for x in list(permution):
#         # print(x)
#         if last_x == None:
#             last_x = x
#             if x > 40:
#                 return False
#         elif x - last_x > 40:
#             return False
#         else:
#             last_x = x
#     if 78-x> 40:
#         return False
#     return True



# def find_best_situation(laps,pit_stops,tires):
#     permutations = itertools.combinations([x+1 for x in range(laps-1)],pit_stops)
#     # return permutations
#     lowest = 100000
#     perm = None
#     for permutation in permutations:
#         if check_possible(permutation):
#             x,y = try_all_tires(permutation,tires,laps,pit_stops)
#             if len(set(y)) >1:
#                 if x + (pit_stops*25) <= lowest:
#                     lowest = x + (pit_stops*25)
#                     print(lowest)
#                     perm = permutation
#                     tire_config = y
#                     print(perm)
#                     print(tire_config)
#     print(lowest)
#     print(perm)
#     print(tire_config)
# def try_all_tires(order,tires,laps,pit_stops):
#     order = list(order)
#     order.append(78)
#     least_time = 1000000
#     final_tires = []
#     for tire_config in POSSIBLE_TIRE_CONFIGS[pit_stops-1]:
#         current_time = 0
#         running_combo = True
#         delta_laps = []
#         x=0
#         for lap in order:
#             delta_laps.append(lap-x)
#             x = lap
#         # print(delta_laps)

#         x = 0
#         finished_combo = False
#         while running_combo:
#             if delta_laps[x] > MAXTIRE[tire_config[x]]:
#                 running_combo = False
#             else:
#                 current_time += tires[tire_config[x]][delta_laps[x]-1]
#                 x+=1
#                 if x == len(delta_laps):
#                     running_combo = False
#                     finished_combo = True
#         if current_time < least_time and finished_combo:
#             least_time = current_time
#             final_tires = tire_config
#         # current_tires = tire_config[0]
#         # for lap in delta_laps:
#             # if lap < 
#             # pass

#         # while running_combo:
            
#     return least_time,final_tires
#     # for a in range(3):
#     #     current_tires = []
#     #     last_lap = 0
#     #     current_time = 0
#     #     current_tire = a
#     #     current_tires.append(current_tire)
#     #     for x in range(len(order)):
#     #         tires_available = []
#     #         for tire in range(3):
#     #             if order[x]-last_lap < MAXTIRE[tire]:
#     #                 tires_available.append(tire)
#     #         least_amount = 1000000000
#     #         tires_used = None
#     #         for tire in tires_available:
#     #             if tires[tire][order[x]-last_lap-1] < least_amount:
#     #                 least_amount = tires[tire][order[x]-last_lap-1]
#     #                 tires_used = tire
#     #         current_time+= least_amount
#     #         current_tires.append(tires_used)
#     #         last_lap=order[x]
#     #     if current_time < least_time:
#     #         least_time = current_time
#     #         current_time = 0
#     #         final_tires = current_tires
#     #     final_tires.pop()
#     return least_time,final_tires
                
            
        

# def make_schedule(tires,laps):
#     current_tires = None
#     timings = []
#     for pit_stops in range(2,16): # number of pit stops
#         timings.append(find_best_situation(laps,pit_stops,tires))


# # def find_best_tire_switch(current_tires,laps_on_tire,laps,tires):
    

# if __name__ == "__main__":
#     laps=78
#     df = open_csv("Monaco+Grand+Prix.csv")
#     tires = make_tires(df)
#     make_schedule(tires,laps)
