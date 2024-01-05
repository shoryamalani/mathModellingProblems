
# Description: This program simulates the population of two planets over time.
def calculate_one_years_migration(percent_from_first_population,percent_from_second_population,first_population,second_population):
    """This function takes in the percentage of people that migrate from the first population to the second population, the percentage of people that migrate from the second population to the first population, the first population, and the second population. It returns the new populations of the first and second planets after one year."""
    temp_first_population = first_population - (first_population * percent_from_first_population) + (second_population * percent_from_second_population)
    temp_second_population = second_population - (second_population * percent_from_second_population) + (first_population * percent_from_first_population)
    return temp_first_population, temp_second_population

def calculate_one_years_migration_three_way(percent_1_2,percent_1_3,percent_2_1,percent_2_3,percent_3_1,percent_3_2,pop_1,pop_2,pop_3):
    """This function takes in the percentage of people that migrate from the first population to the third population, the percentage of people that migrate from the second population to the third population, the percentage of people that migrate from the second population to the first population, the percentage of people that migrate from the second population to the third population, the percentage of people that migrate from the third population to the first population, the percentage of people that migrate from the third population to the second population, the first population, the second population, and the third population. It returns the new populations of the first, second, and third planets after one year."""
    temp_pop_1 = pop_1 - ((pop_1 * percent_1_2) + (pop_1 * percent_1_3)) + ((pop_2 * percent_2_1) + (pop_3 * percent_3_1))
    temp_pop_2 = pop_2 - ((pop_2 * percent_2_1) + (pop_2 * percent_2_3)) + ((pop_1 * percent_1_2) + (pop_3 * percent_3_2))
    temp_pop_3 = pop_3 - ((pop_3 * percent_3_1) + (pop_3 * percent_3_2)) + ((pop_1 * percent_1_3) + (pop_2 * percent_2_3))
    return temp_pop_1, temp_pop_2, temp_pop_3

#same as above but with 4 populations
def calculate_one_years_migration_four_way(percent_1_2,percent_1_3,percent_1_4,percent_2_1,percent_2_3,percent_2_4,percent_3_1,percent_3_2,percent_3_4,percent_4_1,percent_4_2,percent_4_3,pop_1,pop_2,pop_3,pop_4):
    """This function takes in the percentage of people that migrate from the first population to the second population, the percentage of people that migrate from the first population to the third population, the percentage of people that migrate from the first population to the fourth population, the percentage of people that migrate from the second population to the first population, the percentage of people that migrate from the second population to the third population, the percentage of people that migrate from the second population to the fourth population, the percentage of people that migrate from the third population to the first population, the percentage of people that migrate from the third population to the second population, the percentage of people that migrate from the third population to the fourth population, the percentage of people that migrate from the fourth population to the first population, the percentage of people that migrate from the fourth population to the second population, the percentage of people that migrate from the fourth population to the third population, the first population, the second population, the third population, and the fourth population. It returns the new populations of the first, second, third, and fourth planets after one year."""
    temp_pop_1 = pop_1 - ((pop_1 * percent_1_2) + (pop_1 * percent_1_3) + (pop_1 * percent_1_4)) + ((pop_2 * percent_2_1) + (pop_3 * percent_3_1) + (pop_4 * percent_4_1))
    temp_pop_2 = pop_2 - ((pop_2 * percent_2_1) + (pop_2 * percent_2_3) + (pop_2 * percent_2_4)) + ((pop_1 * percent_1_2) + (pop_3 * percent_3_2) + (pop_4 * percent_4_2))
    temp_pop_3 = pop_3 - ((pop_3 * percent_3_1) + (pop_3 * percent_3_2) + (pop_3 * percent_3_4)) + ((pop_1 * percent_1_3) + (pop_2 * percent_2_3) + (pop_4 * percent_4_3))
    temp_pop_4 = pop_4 - ((pop_4 * percent_4_1) + (pop_4 * percent_4_2) + (pop_4 * percent_4_3)) + ((pop_1 * percent_1_4) + (pop_2 * percent_2_4) + (pop_3 * percent_3_4))
    return temp_pop_1, temp_pop_2, temp_pop_3, temp_pop_4





if __name__ == "__main__":
    percent_migration_from_uranus = 0.81
    percent_migration_from_venus = 0.01

    current_year = 0

    uranus_pop = 4000
    venus_pop = 0
    for _ in range(25):
        current_year += 1
        uranus_pop, venus_pop = calculate_one_years_migration(percent_migration_from_uranus,percent_migration_from_venus,uranus_pop,venus_pop)
        print(f"Year {current_year}: {uranus_pop} people on Uranus, {venus_pop} people on Venus")

    # initial populations
    current_year = 0
    green = 300
    independent = 200
    dragon = 300
    green_to_dragon = 0.05
    green_to_independent = 0.20
    independent_to_green = 0.20
    independent_to_dragon = 0.40
    dragon_to_green = 0.20
    dragon_to_independent = 0.20
    for _ in range(25):
        current_year += 1
        green,dragon, independent  = calculate_one_years_migration_three_way(green_to_dragon,green_to_independent,dragon_to_green,dragon_to_independent,independent_to_dragon,independent_to_green,green,dragon,independent)
        print(f"Year {current_year}: {green} people on Green, {independent} people on Independent, {dragon} people on Dragon")
    
    # initial populations
    current_year = 0
    alpha = 300
    bravo = 200
    charlie = 300
    delta = 200
    alpha_to_bravo = 0.05
    alpha_to_charlie = 0.20
    alpha_to_delta = 0.20
    bravo_to_alpha = 0.20
    bravo_to_charlie = 0.40
    bravo_to_delta = 0.20
    charlie_to_alpha = 0.20
    charlie_to_bravo = 0.20
    charlie_to_delta = 0.20
    delta_to_alpha = 0.20
    delta_to_bravo = 0.20
    delta_to_charlie = 0.20
    for _ in range(25):
        current_year += 1
        alpha,bravo,charlie,delta = calculate_one_years_migration_four_way(alpha_to_bravo,alpha_to_charlie,alpha_to_delta,bravo_to_alpha,bravo_to_charlie,bravo_to_delta,charlie_to_alpha,charlie_to_bravo,charlie_to_delta,delta_to_alpha,delta_to_bravo,delta_to_charlie,alpha,bravo,charlie,delta)
        print(f"Year {current_year}: {alpha} people on Alpha, {bravo} people on Bravo, {charlie} people on Charlie, {delta} people on Delta")
        delta -= 5

