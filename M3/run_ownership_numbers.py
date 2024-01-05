# import rough_sales_numbers


# print(rough_sales_numbers.aggregate_miles_traveled_by_owners)
# print(rough_sales_numbers.ownership_data_in_thousands)
# print(rough_sales_numbers.aggregate_miles_traveled_by_owners)

# import helpers
# co2_series = []
# for year in rough_sales_numbers.aggregate_miles_traveled_by_owners:
#     co2_series.append(helpers.distance_traveled_to_emissions_saved(rough_sales_numbers.aggregate_miles_traveled_by_owners[year]))

# print(co2_series)

import seaborn as sns
import matplotlib.pyplot as plt
import constants
l = [2.962028906048016, 2.685121749422897, 4.331505259479717, 3.491671748148144, 3.042120994249823, 2.8752839984056116, 4.183442408569497, 3.642282648688911, 2.985207433718605, 2.456250158354115, 3.9393687637178085, 3.808664512632754, 2.660219950025756, 2.7668438777515765, 4.129878249625004, 4.237023793915718, 3.083376335162893, 3.2792185408363523, 4.332458171841828, 4.208337454822093, 3.752073930285346, 3.7499394263910357, 4.311070545742748, 4.402187330886464, 3.4776224768916197, 2.239922740384615, 2.637218633382642, 3.823655483786611, 4.007187302178322, 3.743804271278971, 3.788762159536541, 4.305172666879256, 4.241091052880659, 4.189645147070952, 4.5763857861707615, 3.3288333798590886, 2.9528688561463046, 3.5153071721698104, 2.6621831950883004, 2.96261584150844, 3.9449289949147, 3.733795974856318, 3.8449477570266226, 3.4945764365476193, 4.035136424486461, 3.4640857233796325, 3.730316008333332, 3.1328862274408293, 3.422466868489584, 2.396770028034979, 2.6276355888324883, 2.4933656814138585, 4.419082263036812, 6.501465376666666, 6.877070751398212, 5.304492430685358, 8.740786695906433, 8.290282975529097, 4.814407665833335, 5.823901166485514, 3.5250485230952386, 3.2787139488993717, 2.776983225833332, 3.444004793803418, 3.806908671296295, 4.498179463133639, 4.7114642896981636, 4.055366112424239, 4.257228711004272, 3.53035403416054, 4.489388041666664, 3.9535138028455292, 4.020662224862258, 3.1246087406195464, 2.921043539772727, 3.3305848647186154, 4.111367381233595, 4.848136749999998, 5.319490929804801, 3.983314228739316, 5.2755325912648106, 4.179636214726635, 3.7551961545768555, 4.028706411911911, 3.870836665224361, 3.65053872547619, 3.4080469881535933]
l= l[25:]
print(l)
import helpers
l = [helpers.distance_traveled_to_emissions_saved(x) for x in l]
year = 2018
b = []
for a in range(37):
    b.append(l[a] * constants.shared_ridership_total[int(2018 + a/12)] * 12 * 1000)


sns.lineplot(x=range(37), y=b)
plt.xlabel = "Months since 2018"
plt.ylabel = "CO2 Emissions Saved (tons)"
plt.savefig("test.png")