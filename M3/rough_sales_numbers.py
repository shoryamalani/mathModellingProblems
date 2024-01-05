# using sales numbers to estimate ownership and usage
import pandas as pd
import constants

sales_data_in_thousands = pd.Series({2012:70,
2013:159,
2014:193,
2015:130,
2016:152,
2017:(152 + 369) /2, # imputing the average between the two
2018:369,
2019:423,
2020:416,
2021:750,
2022:928,
})
sales_data_in_thousands = pd.DataFrame(sales_data_in_thousands)



def aggregate_sales_numbers(sales_data: pd.DataFrame):
    """
    We are assuming that a total number of ebike sales is a good number for owners
    """
    return_df = sales_data.copy()
    running_total = 0
    totals = []
    for x,y in sales_data.iterrows():
        running_total += y[0]
        print(x,y[0])
        totals.append(running_total)
    return totals


def aggregate_miles_traveled_by_owners_yearly(ownership_data) -> pd.DataFrame:
    """
    getting the aggregate data traveled by owners yearly
    ownership data: ownership data in thousands
    """
    final = []
    data_f = {

    }
    year = 2012
    for val in ownership_data:
        num_riding_miles = val * constants.avg_miles_covered_per_day_by_ebike_owners * 365.25 * 1000 # num minutes covered in a year
        data_f[year] = num_riding_miles
        year += 1
    return data_f

ownership_data_in_thousands = aggregate_sales_numbers(sales_data_in_thousands)
print(ownership_data_in_thousands)

aggregate_miles_traveled_by_owners = aggregate_miles_traveled_by_owners_yearly(ownership_data_in_thousands)
print(aggregate_miles_traveled_by_owners)