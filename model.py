import random
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use("classic")

# Global Initial Variables
# growth_rate is for the wood market
growth_rate = 1.03
# growth_rate_2 is for the non wood market
growth_rate_2 = 1.02
# inflation_rate
initial_inflation_rate = 1.02
# Demand growth can be found in the specific function

# Sets the initial amount the megatrend should have for the first iteration in the model
initial_megatrend = 50

# Initial Supplies
# Values below are tons
initial_supply_of_wood = 16790000
# 7.4 million tons get manufactured each year in austria
initial_supply_of_steel = 7400000
# ratio supply_of_steel  / 35 for aluminium
initial_supply_of_aluminium = 200000
# as stated in the "WKO-Report"
initial_supply_of_glass = 524000
# In Germany 17.9 million tons supply of plastics --> 10% for Austria
initial_supply_of_plastics = 1790000

# Initial Prices in €
initial_price_of_wood = 100
initial_price_steel = 424.16
initial_price_aluminium = 2529.51
# Germany - statistics "Complete Revenue": 1321 € per ton
# Austria - "WKO branchen-industry report": 1950 € per ton
initial_price_glass = 1975
initial_price_plastics = 938.67

# Variable to fluctuate the demand for wood furniture
# default = False
material_trends = False

# variable to fluctuate the current policies in the austrian government
# if pro environmental policies should not only continually rise
# displays the changing politic interest
# event trigger for pro environmental policy fluctuation
# default = False
policy_fluctuation = False

# event trigger for extreme inflation
# default = False
extreme_inflation = False

# event trigger for supply crisis: wood
# default = False
supply_crisis_wood = False

# event trigger for supply crisis: aluminium
# default = False
supply_crisis_aluminium = False


def calculate_megatrend(index, megatrends):

    value_megatrends = megatrends * ((index/50) + 1)

    return value_megatrends


def calculate_pro_environmental_policies(megatrends, year, election_results):

    election_results_list = election_results
    if policy_fluctuation:
        # year == 2 --> 2024: "Nationalratswahl"
        # year == 7 --> 2029: "Nationalratswahl"
        if year == 2 or year == 7:
            fluctuation = round(random.uniform(-0.1, 0.1),4)
            election_results_list.append(fluctuation)
            policy_fluctuation_variable = 0 + fluctuation
        elif year > 2 and year <= 6:
            policy_fluctuation_variable = election_results_list[0]
        elif year > 7 and year <= 11:
            policy_fluctuation_variable = election_results_list[1]
        else:
            policy_fluctuation_variable = 0
    else:
        policy_fluctuation_variable = 0

    pro_environmental_policies = (0.5 + (megatrends/95)) + policy_fluctuation_variable

    return pro_environmental_policies, election_results_list


def calculate_supply_of_wood(year, growth_rate, current_supply_of_wood):

    crisis_year = 2
    min_value = 1.05
    max_value = 1.1

    if supply_crisis_wood and year == crisis_year:
        decrease = random.uniform(min_value, max_value)
        print(f"current_supply_of_wood before decrease: {current_supply_of_wood} tons.")
        current_supply_of_wood_return = growth_rate * (current_supply_of_wood / decrease)
        print(f"Current supply of wood after decrease: {current_supply_of_wood_return} tons. Wood supply decrease in: {(decrease - 1)*100}%.")
    else:
        current_supply_of_wood_return = growth_rate * current_supply_of_wood

    return current_supply_of_wood_return


def calculate_supply_of_non_wood_m(year, current_supply_of_steel, current_supply_of_aluminium,
                                   current_supply_of_glass, current_supply_of_plastics, growth_rate_2):

    crisis_year = 3
    min_value = 1.05
    max_value = 1.3

    if supply_crisis_aluminium and year == crisis_year:
        decrease = random.uniform(min_value, max_value)
        print(f"Aluminium supply before decrease: {decrease}.")
        current_supply_of_aluminium = growth_rate_2 * (current_supply_of_aluminium / decrease)
        print(f"Aluminium supply after decrease: {decrease}. Aluminium supply decrease in: {(decrease - 1)*100}%.")
    else:
        current_supply_of_steel = (growth_rate_2 * current_supply_of_steel)
        current_supply_of_aluminium = (growth_rate_2 * current_supply_of_aluminium)
        current_supply_of_glass = (growth_rate_2 * current_supply_of_glass)
        current_supply_of_plastics = (growth_rate_2 * current_supply_of_plastics)

    return current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics


def calculate_price_of_wood_m(inflation_rate, year, price_of_wood, current_supply_of_wood,
                              value_current_supply_of_wood):

    # Is a support variable, to get access data of the last year in request lists
    iteration = year - 1

    # Is needed to regulate market consequences
    impact = 1.03

    if year == 0:
        price_of_wood = price_of_wood
    else:
        price_of_wood = ((price_of_wood / (current_supply_of_wood / value_current_supply_of_wood[iteration])) *
                         inflation_rate) * impact

    return price_of_wood


def calculate_price_of_non_wood_m(inflation_rate, year, price_of_steel, price_of_aluminium, price_of_glass,
                                  price_of_plastics, pro_environmental_policies, current_supply_of_steel,
                                  value_current_supply_of_steel, current_supply_of_aluminium,
                                  value_current_supply_of_aluminium, current_supply_of_glass,
                                  value_current_supply_of_glass, current_supply_of_plastics,
                                  value_current_supply_of_plastics):

    # Is a support variable, to get access data of the last year in request lists
    iteration = year - 1

    # Variable is needed so the ratio steel can be calculated at the end of the function
    old_price_of_steel = price_of_steel

    # price increase due to pro environmental policies
    if pro_environmental_policies < 1:
        price_increase = 1
    elif pro_environmental_policies >= 1 and pro_environmental_policies < 1.1:
        price_increase = 1.05
    elif pro_environmental_policies >= 1.1 and pro_environmental_policies <= 1.18:
        price_increase = 1.1
    else:
        price_increase = 1.2

    if year == 0:
        price_of_steel = price_of_steel
        price_of_aluminium = price_of_aluminium
        price_of_glass = price_of_glass
        price_of_plastics = price_of_plastics
    else:
        price_of_steel = price_of_steel / (current_supply_of_steel /
                                           value_current_supply_of_steel[iteration]) * inflation_rate * price_increase
        price_of_aluminium = price_of_aluminium / (current_supply_of_aluminium /
                                                   value_current_supply_of_aluminium[iteration]) * inflation_rate * \
                             price_increase
        price_of_glass = price_of_glass / (current_supply_of_glass /
                                           value_current_supply_of_glass[iteration]) * inflation_rate * price_increase
        price_of_plastics = price_of_plastics / (current_supply_of_plastics /
                                                 value_current_supply_of_plastics[iteration]) * inflation_rate * \
                            price_increase

    ratio_steel = price_of_steel/old_price_of_steel

    return price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics, ratio_steel


def calculate_demand_for_wood_furniture(year, megatrends):

    crisis_year1_bool = True
    crisis_year2_bool = True
    crisis_year1 = 2
    crisis_year2 = 6
    min_value = -15
    max_value = 15

    if material_trends and year == crisis_year1 and crisis_year1_bool:
        material_trends_variable = random.choice([min_value, max_value]) / 100
        print(f"Material trends: {material_trends_variable * 100}%.")
    elif material_trends and year == crisis_year2 and crisis_year2_bool:
        material_trends_variable = random.choice([min_value, max_value]) / 100
        print(f"Material trends: {material_trends_variable * 100}%.")
    else:
        material_trends_variable = 0

    if megatrends >= 50:
        ratio_for_wood_furniture_demand_ = (megatrends / 500 + 1) + material_trends_variable
    else:
        ratio_for_wood_furniture_demand_ = (1 - (megatrends / 500)) + material_trends_variable

    return ratio_for_wood_furniture_demand_


def calculate_used_wood_for_furniture(year, value_wood_demand_, price_of_wood, value_price_of_wood,
                                      ratio_for_wood_furniture_demand,
                                      ratio_steel):

    # Is a support variable, to get access data of the last year in request lists
    iteration = year - 1

    # Variable boost price impact
    price_impact_influence = 2

    if year == 0:
        used_wood_for_furniture = value_wood_demand_[year]
    else:
        price_difference_wood = price_of_wood / value_price_of_wood[iteration]
        price_difference_wood = (price_difference_wood * price_impact_influence) - 1
        used_wood_for_furniture = value_wood_demand_[year] / price_difference_wood * ratio_for_wood_furniture_demand * \
                                  ratio_steel

    return used_wood_for_furniture


def calculate_used_non_wood_material(year, value_price_of_steel, price_of_steel, value_steel_demand_,
                                     value_price_of_aluminium, price_of_aluminium, value_aluminium_demand_,
                                     value_price_of_glass, price_of_glass, value_glass_demand_,
                                     value_price_of_plastics, price_of_plastics, value_plastics_demand_,
                                     price_of_wood, ratio_for_wood_furniture_demand, value_price_of_wood):

    # Is a support variable, to get access data of the last year in request lists
    iteration = year - 1

    # Variable boost price impact
    price_impact_influence = 2

    if year == 0:
        used_steel_for_furniture = value_steel_demand_[year]
        used_aluminium_for_furniture = value_aluminium_demand_[year]
        used_glass_for_furniture = value_glass_demand_[year]
        used_plastics_for_furniture = value_plastics_demand_[year]
    else:
        ratio_wood_price = price_of_wood / value_price_of_wood[iteration]

        ratio_for_wood_furniture_demand = (ratio_for_wood_furniture_demand / 4) + 0.75

        price_difference_steel = price_of_steel / value_price_of_steel[iteration]
        price_difference_steel = (price_difference_steel * price_impact_influence) - 1
        used_steel_for_furniture = value_steel_demand_[year] / price_difference_steel * ratio_wood_price \
                                   / ratio_for_wood_furniture_demand

        price_difference_aluminium = price_of_aluminium / value_price_of_aluminium[iteration]
        price_difference_aluminium = (price_difference_aluminium * price_impact_influence) - 1
        used_aluminium_for_furniture = value_aluminium_demand_[year] / price_difference_aluminium * ratio_wood_price \
                                       / ratio_for_wood_furniture_demand

        price_difference_glass = price_of_glass / value_price_of_glass[iteration]
        price_difference_glass = (price_difference_glass * price_impact_influence) - 1
        used_glass_for_furniture = value_glass_demand_[year] / price_difference_glass * ratio_wood_price \
                                   / ratio_for_wood_furniture_demand

        price_difference_plastics = price_of_plastics / value_price_of_plastics[iteration]
        price_difference_plastics = (price_difference_plastics * price_impact_influence) - 1
        used_plastics_for_furniture = value_plastics_demand_[year] / price_difference_plastics * ratio_wood_price \
                                      / ratio_for_wood_furniture_demand

    return used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture


def calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture,
                    used_glass_for_furniture, used_plastics_for_furniture):

    sum_used_wood = used_wood_for_furniture
    sum_non_wood = used_steel_for_furniture + used_aluminium_for_furniture + used_glass_for_furniture + \
                   used_plastics_for_furniture

    return sum_used_wood / (sum_used_wood + sum_non_wood)


def calculate_global_warming_potential(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture,
                                       used_glass_for_furniture, used_plastics_for_furniture):
    # kg Co2 per tonne
    steel = 1.836

    # kg Co2 per tonne
    plastic = 3.451

    # kg Co2 per tonne
    glass = 1.031

    # kg Co2 per tonne
    wood = 0.283

    # kg Co2 per tonne
    aluminium = 10.546

    gwp = used_wood_for_furniture * wood + used_steel_for_furniture * steel + used_aluminium_for_furniture * \
          aluminium + used_plastics_for_furniture * plastic + used_glass_for_furniture * glass

    return gwp


def create_price_subplots(data_dic, **plot_params):

    fig, ax = plt.subplots(8, figsize=(22,22))
    # fig.suptitle('Overview Prices')
    fig.tight_layout(pad=3.0)
    # plt.grid(color='b', linestyle='-', linewidth=0.1)
    ax[0].plot(data_dic["value_time"], data_dic["value_megatrends"], **plot_params)
    ax[0].set_title("megatrends")
    ax[1].plot(data_dic["value_time"], data_dic["value_index"], **plot_params)
    ax[1].set_title("index")
    ax[2].plot(data_dic["value_time"], data_dic["value_pro_environmental_policies"], **plot_params)
    ax[2].set_title("pro_environmental_policies")
    ax[3].plot(data_dic["value_time"], data_dic["value_price_of_wood"], **plot_params)
    ax[3].set_title("value_price_of_wood (€)")
    ax[4].plot(data_dic["value_time"], data_dic["value_price_of_steel"], **plot_params)
    ax[4].set_title("value_price_of_steel (€)")
    ax[5].plot(data_dic["value_time"], data_dic["value_price_of_aluminium"], **plot_params)
    ax[5].set_title("value_price_of_aluminium (€)")
    ax[6].plot(data_dic["value_time"], data_dic["value_price_of_glass"], **plot_params)
    ax[6].set_title("value_price_of_glass (€)")
    ax[7].plot(data_dic["value_time"], data_dic["value_price_of_plastics"], **plot_params)
    ax[7].set_title("value_price_of_plastics (€)")
    for i in range(8):
        ax[i].grid()
    plt.savefig("static/overview_prices")
    plt.close()
    plt.show()


def create_material_supply_subplot(data_dic, **plot_params):
    fig, ax = plt.subplots(8, figsize=(22,22))
    # fig.suptitle('Current Material Supplies')
    fig.tight_layout(pad=3.0)
    # plt.grid(color='b', linestyle='-', linewidth=0.1)
    ax[0].plot(data_dic["value_time"], data_dic["value_megatrends"], **plot_params)
    ax[0].set_title("megatrends")
    ax[1].plot(data_dic["value_time"], data_dic["value_index"], **plot_params)
    ax[1].set_title("index")
    ax[2].plot(data_dic["value_time"], data_dic["value_pro_environmental_policies"], **plot_params)
    ax[2].set_title("pro_environmental_policies")
    ax[3].plot(data_dic["value_time"], data_dic["value_current_supply_of_wood"], **plot_params)
    ax[3].set_title("value_current_supply_of_wood (tons)")
    ax[4].plot(data_dic["value_time"], data_dic["value_current_supply_of_steel"], **plot_params)
    ax[4].set_title("value_current_supply_of_steel (tons)")
    ax[5].plot(data_dic["value_time"], data_dic["value_current_supply_of_aluminium"], **plot_params)
    ax[5].set_title("value_current_supply_of_aluminium (tons)")
    ax[6].plot(data_dic["value_time"], data_dic["value_current_supply_of_glass"], **plot_params)
    ax[6].set_title("value_current_supply_of_glass (tons)")
    ax[7].plot(data_dic["value_time"], data_dic["value_current_supply_of_plastics"], **plot_params)
    ax[7].set_title("value_current_supply_of_plastics (tons)")
    for i in range(8):
        ax[i].grid()
    plt.savefig("static/current_material_supplies")
    plt.close()
    plt.show()


def create_used_materials_and_emissions_subplots(data_dic, **plot_params):

    fig, ax = plt.subplots(9, figsize=(22,22))
    # fig.suptitle('Used Materials + Emissions')
    fig.tight_layout(pad=3.0)
    # plt.grid(color='b', linestyle='-', linewidth=0.1)
    ax[0].plot(data_dic["value_time"], data_dic["value_megatrends"], **plot_params)
    ax[0].set_title("megatrends")
    ax[1].plot(data_dic["value_time"], data_dic["value_index"], **plot_params)
    ax[1].set_title("index")
    ax[2].plot(data_dic["value_time"], data_dic["value_pro_environmental_policies"], **plot_params)
    ax[2].set_title("pro_environmental_policies")
    ax[3].plot(data_dic["value_time"], data_dic["value_used_wood_for_furniture"], **plot_params)
    ax[3].set_title("value_used_wood_for_furniture (tons)")
    ax[4].plot(data_dic["value_time"], data_dic["value_used_steel_for_furniture"], **plot_params)
    ax[4].set_title("value_used_steel_for_furniture (tons)")
    ax[5].plot(data_dic["value_time"], data_dic["value_used_aluminium_for_furniture"], **plot_params)
    ax[5].set_title("value_used_aluminium_for_furniture (tons)")
    ax[6].plot(data_dic["value_time"], data_dic["value_used_glass_for_furniture"], **plot_params)
    ax[6].set_title("value_used_glass_for_furniture (tons)")
    ax[7].plot(data_dic["value_time"], data_dic["value_used_plastics_for_furniture"], **plot_params)
    ax[7].set_title("value_used_plastics_for_furniture (tons)")
    ax[8].plot(data_dic["value_time"], data_dic["value_gwp"], **plot_params)
    ax[8].set_title("KG CO2 eq. emitted (per year)")
    for i in range(9):
        ax[i].grid()
    plt.savefig("static/used_materials_and_emissions")
    plt.close()
    plt.show()


def calculate_extreme_inflation():

    inflation_rate = 1 + (random.gauss(12, 4) / 100)

    print(f"inflation_rate: {inflation_rate}")

    return inflation_rate


def calculate_demand(year_, value_wood_demand_, value_steel_demand_, value_aluminium_demand_, value_glass_demand_,
                     value_plastics_demand_):

    # Value below is tons
    industry_wood_demand = 132593

    # Current assumption is 80% aluminium and 20% steel
    ratio_metals = 33805
    industry_steel_demand = ratio_metals * 0.2
    industry_aluminium_demand = ratio_metals * 0.8

    # Values are calculated from data as: "gütereinsatzstatistik / preis"
    industry_glass_demand = 6890
    industry_plastics_demand = 45715

    # demand growth rate displays industry demand growth per year
    demand_growth_rate = 1.03

    # Is a support variable, to get access data of the last year in request lists
    iteration = year_ - 1

    if year_ == 0:
        value_wood_demand_.append(industry_wood_demand)
        value_steel_demand_.append(industry_steel_demand)
        value_aluminium_demand_.append(industry_aluminium_demand)
        value_glass_demand_.append(industry_glass_demand)
        value_plastics_demand_.append(industry_plastics_demand)
    else:
        value_wood_demand_.append(value_wood_demand_[iteration] * demand_growth_rate)
        value_steel_demand_.append(value_steel_demand_[iteration] * demand_growth_rate)
        value_aluminium_demand_.append(value_aluminium_demand_[iteration] * demand_growth_rate)
        value_glass_demand_.append(value_glass_demand_[iteration] * demand_growth_rate)
        value_plastics_demand_.append(value_plastics_demand_[iteration] * demand_growth_rate)

    return value_wood_demand_, value_steel_demand_, value_aluminium_demand_, value_glass_demand_, value_plastics_demand_


def run(counter):

    # dv = decimal values
    dv = 2

    megatrends = initial_megatrend
    current_supply_of_wood = initial_supply_of_wood
    current_supply_of_steel = initial_supply_of_steel
    current_supply_of_aluminium = initial_supply_of_aluminium
    current_supply_of_glass = initial_supply_of_glass
    current_supply_of_plastics = initial_supply_of_plastics
    price_of_wood = initial_price_of_wood
    price_of_steel = initial_price_steel
    price_of_aluminium = initial_price_aluminium
    price_of_glass = initial_price_glass
    price_of_plastics = initial_price_plastics
    inflation_rate = initial_inflation_rate

    # here initial lists get created so we can store the model data during the for loop
    value_time = []
    value_megatrends = []
    value_pro_environmental_policies = []
    value_current_supply_of_wood = []
    value_price_of_wood = []
    value_current_supply_of_steel, value_current_supply_of_aluminium, value_current_supply_of_glass, value_current_supply_of_plastics = [], [], [], []
    value_price_of_steel, value_price_of_aluminium, value_price_of_glass, value_price_of_plastics = [], [], [], []
    value_used_wood_for_furniture = []
    value_used_steel_for_furniture, value_used_aluminium_for_furniture, value_used_glass_for_furniture, value_used_plastics_for_furniture = [], [], [], []
    value_index = []
    value_gwp = []
    election_results = []
    value_wood_demand = []
    value_steel_demand = []
    value_aluminium_demand = []
    value_glass_demand = []
    value_plastics_demand = []

    for year in range(counter):
        print(f"Run: {year} "+ " / Year: " + str(2022 + year))

        if extreme_inflation:
            inflation_rate = calculate_extreme_inflation()
        else:
            inflation_rate = inflation_rate

        value_wood_demand, value_steel_demand, value_aluminium_demand, value_glass_demand, value_plastics_demand = calculate_demand(year, value_wood_demand, value_steel_demand, value_aluminium_demand, value_glass_demand, value_plastics_demand)

        pro_environmental_policies, election_results = calculate_pro_environmental_policies(megatrends, year, election_results)

        current_supply_of_wood = calculate_supply_of_wood(year, growth_rate, current_supply_of_wood)

        price_of_wood = calculate_price_of_wood_m(inflation_rate, year, price_of_wood, current_supply_of_wood, value_current_supply_of_wood)

        current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics = calculate_supply_of_non_wood_m(year, current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics, growth_rate_2)

        price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics, ratio_steel = calculate_price_of_non_wood_m(inflation_rate, year, price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics, pro_environmental_policies, current_supply_of_steel, value_current_supply_of_steel, current_supply_of_aluminium, value_current_supply_of_aluminium, current_supply_of_glass, value_current_supply_of_glass, current_supply_of_plastics, value_current_supply_of_plastics)

        ratio_for_wood_furniture_demand = calculate_demand_for_wood_furniture(year, megatrends)

        used_wood_for_furniture = calculate_used_wood_for_furniture(year, value_wood_demand, price_of_wood, value_price_of_wood, ratio_for_wood_furniture_demand, ratio_steel)

        used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture = calculate_used_non_wood_material(year, value_price_of_steel, price_of_steel, value_steel_demand,value_price_of_aluminium, price_of_aluminium, value_aluminium_demand, value_price_of_glass, price_of_glass, value_glass_demand, value_price_of_plastics, price_of_plastics, value_plastics_demand, price_of_wood, ratio_for_wood_furniture_demand, value_price_of_wood)

        index = calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture)

        megatrends = calculate_megatrend(index, megatrends)

        gwp = calculate_global_warming_potential(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture)
        gwp = round(gwp, dv)
        print("______________________")

        value_time.append(year + 1)
        value_price_of_wood.append(round(price_of_wood, dv))
        value_index.append(round(index, dv))
        value_pro_environmental_policies.append(round(pro_environmental_policies, dv))
        value_megatrends.append(round(megatrends, dv))
        value_price_of_steel.append(round(price_of_steel, dv))
        value_price_of_aluminium.append(round(price_of_aluminium,dv))
        value_price_of_glass.append(round(price_of_glass, dv))
        value_price_of_plastics.append(round(price_of_plastics, dv))
        value_current_supply_of_wood.append(round(current_supply_of_wood, dv))
        value_current_supply_of_steel.append(round(current_supply_of_steel, dv))
        value_current_supply_of_aluminium.append(round(current_supply_of_aluminium, dv))
        value_current_supply_of_glass.append(round(current_supply_of_glass, dv))
        value_current_supply_of_plastics.append(round(current_supply_of_plastics, dv))
        value_used_wood_for_furniture.append(round(used_wood_for_furniture, dv))
        value_used_steel_for_furniture.append(round(used_steel_for_furniture, dv))
        value_used_aluminium_for_furniture.append(round(used_aluminium_for_furniture, dv))
        value_used_glass_for_furniture.append(round(used_glass_for_furniture, dv))
        value_used_plastics_for_furniture.append(round(used_plastics_for_furniture, dv))
        value_gwp.append(gwp)

    data_dict_ = {"value_time": value_time,
                "value_index": value_index,
                "value_pro_environmental_policies": value_pro_environmental_policies,
                "value_megatrends": value_megatrends,
                "value_price_of_wood": value_price_of_wood,
                "value_price_of_steel": value_price_of_steel,
                "value_price_of_aluminium": value_price_of_aluminium,
                "value_price_of_glass": value_price_of_glass,
                "value_price_of_plastics": value_price_of_plastics,
                "value_current_supply_of_wood": value_current_supply_of_wood,
                "value_current_supply_of_steel": value_current_supply_of_steel,
                "value_current_supply_of_aluminium": value_current_supply_of_aluminium,
                "value_current_supply_of_glass": value_current_supply_of_glass,
                "value_current_supply_of_plastics": value_current_supply_of_plastics,
                "value_used_wood_for_furniture": value_used_wood_for_furniture,
                "value_used_steel_for_furniture": value_used_steel_for_furniture,
                "value_used_aluminium_for_furniture": value_used_aluminium_for_furniture,
                "value_used_glass_for_furniture": value_used_glass_for_furniture,
                "value_used_plastics_for_furniture": value_used_plastics_for_furniture,
                "value_gwp": value_gwp}

    return data_dict_


if __name__ == "__main__":

    print("\nSystem message: Creating Data Dict ...\n")

    data_dict = run(10)

    print("\nSystem message: Data Dict created!\n")

    print("\nSystem message: Creating plots ...\n")

    create_price_subplots(data_dict, marker="D", markerfacecolor="purple", linestyle=':')
    create_material_supply_subplot(data_dict, marker="D", markerfacecolor="purple", linestyle=':')
    create_used_materials_and_emissions_subplots(data_dict, marker="D", markerfacecolor="purple", linestyle=':')

    print("\nSystem message: Plots created and saved!\n")

    print("\nSystem message: Creating Simulation Dataframe ...\n")

    df = pd.DataFrame(data_dict, dtype=float)

    df.to_csv("static/simulation.csv", index=False, sep=";")

    print("\nSystem message: Simulation Dataframe created and saved!\n")

    # uncomment if you want to inspect the dataframe
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(colored("\nSystem message: Dataframe:")
    # print(df)

