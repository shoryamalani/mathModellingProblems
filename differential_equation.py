
import math
start_pop = 309
end_pop = 326
t = 7
k = (1/t)*math.log(end_pop/start_pop)
precision = 100000
x = 0
y = start_pop
years = 50
reached = False
for year in range(years):
    for a in range(0,precision):
        x += 1/precision
        y += k*y*(1/precision)
    print(y)
    if y > 400 and not reached:
        reached = True
        print ("The population will exceed 400 million in", year + 2017)
print(y)
print(k)

inPatient = 0
for i in range(10000):
    inPatient += 150
    inPatient -= 0.45*inPatient
print(inPatient)

start_balance = 500
interest_rate = 0.02
payment = 35
tot_pay = 0
while(start_balance>0):
    start_balance += start_balance*interest_rate
    start_balance -= payment
    tot_pay += payment
    # print(start_balance)
print(tot_pay+start_balance)