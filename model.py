import random
import matplotlib.pyplot as plt
import pandas as pd
from termcolor import colored
plt.style.use("classic")


# Global Initial Variables
# growth_rate is for the wood market
growth_rate = 1.025
# growth_rate_2 is for the non wood market
growth_rate_2 = 1.02

# Sets the initial amount the megatrend should have for the first iteration in the model
# the higher the megatrend, the higher environmental policies, the cheaper the price of wood
initial_megatrend = 50

# Values below are tons
initial_amount_of_wood = 16790000
industry_wood_demand = 132593

# Current assumption is 80% aluminium and 20% steel
ratio_metals = 33805
# Values below are tons and flexible because the dependency to the ratio_metals variable
industry_steel_demand = ratio_metals * 0.2
industry_aluminium_demand = ratio_metals * 0.8

# Values are calculated from data as: "gütereinsatzstatistik / preis"
industry_glass_demand = 6890
industry_placstics_demand = 45715

# Initial Supplies
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
# Germany - statistics Gesamtumsatz: 1321 € per ton
# Austria - WKO branchenindustry: 1950 € per ton
initial_price_glass = 1975
initial_price_plastics = 938.67

# Variable to fluctuate the demand for wood materials
# default = False
# TODO: Look how much the market changed and fluctuated over time in the real market
material_trends = False

# variable to fluctuate the current policies in the austrian government
# if policies should not only continually rise - displays the changing interest within politic interest
# default = False
policy_fluctuation = False

# Initial seed for random values (NOT YET IMPLEMENTED - JUST A PLACEHOLDER)
# seed = 10


def calculate_megatrend(index, megatrends):
    """
    This function calculates the parameter megatrends
    :param index: is the index of how much wood is used in the market
    :param megatrends: shows a general want in society for more sustainability
    :return: the calculated value for megatrends
    """

    # TODO Rückkopplung ok?
    # TODO Weitere Überlegung bzgl. Berechnung --> Positive Rückkopplung: mehr supply of wood,
    # TODO sinkt holzpreis (...) steigert den index, steigert den megatrend usw.

    value_megatrends = megatrends * ((index/100) + 1)
    return value_megatrends


def calculate_pro_environmental_policies(megatrends, year, election_results):
    """
    This function calculates the pro_environmental_policies. It is also provided with the possibility
    of events, if the event triggers are set to True.
    :param megatrends: gets passed to the function when called
    :param year: is the counter of the for main model loop so we can check in which iteration we are and use it for events
    :param election_results: is a list that stores the fluctuation parameter if year == 2 and year == 4
    :return: returns the calculated value for pro_environmental_policies and the list election_results
    """
    election_results_list = election_results
    if policy_fluctuation:
        # year == 2 --> 2024: Nationalratswahl
        # year == 7 --> 2029: Nationalratswahl
        if year == 2 or year == 7:
            fluctuation = round(random.uniform(-0.05, 0.05),4)
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

    # TODO Calculation for pro_environmental_policies could be more sophisticated
    pro_environmental_policies = (0.5 + (megatrends/100)) + policy_fluctuation_variable

    return pro_environmental_policies, election_results_list


def calculate_supply_of_wood(pro_environmental_policies, growth_rate, current_supply_of_wood):
    # formula for: current_supply_of_wood
    current_supply_of_wood_return = pro_environmental_policies * growth_rate * current_supply_of_wood
    return current_supply_of_wood_return


def calculate_supply_of_non_wood_m(pro_environmental_policies, current_supply_of_steel, current_supply_of_aluminium,
                                   current_supply_of_glass, current_supply_of_plastics, growth_rate_2):

    current_supply_of_steel = (growth_rate_2 * current_supply_of_steel) / pro_environmental_policies
    current_supply_of_aluminium = (growth_rate_2 * current_supply_of_aluminium) / pro_environmental_policies
    current_supply_of_glass = (growth_rate_2 * current_supply_of_glass) / pro_environmental_policies
    current_supply_of_plastics = (growth_rate_2 * current_supply_of_plastics) / pro_environmental_policies


    return current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics


def calculate_price_of_wood_m(initial_price_of_wood, current_supply_of_wood, initial_amount_of_wood):
    # formula for: price_of_wood
    price_of_wood = ((initial_price_of_wood) / (current_supply_of_wood / initial_amount_of_wood))
    return price_of_wood


def calculate_price_of_non_wood_m(initial_price_of_wood, price_of_wood, initial_price_steel,
                                  current_supply_of_steel, initial_supply_of_steel, initial_price_aluminium,
                                  current_supply_of_aluminium, initial_supply_of_aluminium, initial_price_glass,
                                  current_supply_of_glass, initial_supply_of_glass, initial_price_plastics,
                                  current_supply_of_plastics, initial_supply_of_plastics):

    ratio_wood = price_of_wood/initial_price_of_wood
    if ratio_wood >= 1:
        ratio_wood -= random.uniform(0, 0.05)
    else:
        ratio_wood += random.uniform(0, 0.05)

    # print("ratio_wood:")
    # print(ratio_wood)

    price_of_steel = ((initial_price_steel) / (current_supply_of_steel/initial_supply_of_steel)) / ratio_wood
    price_of_aluminium = (initial_price_aluminium) / (current_supply_of_aluminium / initial_supply_of_aluminium) / ratio_wood
    price_of_glass = (initial_price_glass) / (current_supply_of_glass / initial_supply_of_glass) / ratio_wood
    price_of_plastics = (initial_price_plastics) / (current_supply_of_plastics / initial_supply_of_plastics) / ratio_wood

    ratio_steel = initial_price_steel/price_of_steel
    if ratio_steel >= 1:
        ratio_steel -= random.uniform(0, 0.05)
    else:
        ratio_steel += random.uniform(0, 0.05)

    return price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics, ratio_steel


def calculate_demand_for_furniture(megatrends):

    # this material_trends_variable will change the demand so that
    # random furniture design trends can be implemented into the model
    # material_trends_variable should give the market demand some variety

    if material_trends:
        material_trends_variable = 0 + random.uniform(-0.15, 0.15)
    else:
        material_trends_variable = 0

    if megatrends >= 50:
        demand_for_furniture = (megatrends / 1000 + 1) + material_trends_variable
    else:
        demand_for_furniture = (1 - (megatrends / 1000)) + material_trends_variable

    return demand_for_furniture


def calculate_amount_of_wood_supply(pro_environmental_policies, current_stock_wood_supply, growth_rate):

    inflow = current_stock_wood_supply * pro_environmental_policies * growth_rate
    outflow = initial_amount_of_wood
    current_stock_wood_supply = inflow - outflow

    return current_stock_wood_supply


def calculate_stock_amount_of_wood_material(industry_wood_demand, price_of_wood, ratio_for_wood_furniture_demand,
                                            initial_price_of_wood, ratio_steel):

    used_wood_for_furniture = (industry_wood_demand / (price_of_wood / initial_price_of_wood) * ratio_for_wood_furniture_demand) * ratio_steel
    return used_wood_for_furniture


def calculate_stock_amount_of_non_wood_material(initial_price_steel, price_of_steel,industry_steel_demand,
                                                initial_price_aluminium, price_of_aluminium, industry_aluminium_demand,
                                                initial_price_glass, price_of_glass, industry_glass_demand,
                                                initial_price_plastics, price_of_plastics, industry_placstics_demand,
                                                price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood):

    ratio_wood_price = price_of_wood/initial_price_of_wood

    # TODO: Check if a price of wood influence is needed here for the model

    used_steel_for_furniture = (industry_steel_demand / (price_of_steel / initial_price_steel) / ratio_for_wood_furniture_demand) * ratio_wood_price
    used_aluminium_for_furniture = (industry_aluminium_demand / (price_of_aluminium / initial_price_aluminium) / ratio_for_wood_furniture_demand) * ratio_wood_price
    used_glass_for_furniture = (industry_glass_demand / (price_of_glass / initial_price_glass) / ratio_for_wood_furniture_demand) * ratio_wood_price
    used_plastics_for_furniture = (industry_placstics_demand / (price_of_plastics / initial_price_plastics) / ratio_for_wood_furniture_demand) * ratio_wood_price

    return used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture


def calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture,
                    used_glass_for_furniture, used_plastics_for_furniture):

    sum_used_wood = used_wood_for_furniture
    sum_non_wood = used_steel_for_furniture + used_aluminium_for_furniture + used_glass_for_furniture + used_plastics_for_furniture
    return sum_used_wood / (sum_used_wood + sum_non_wood)


def calculate_global_warming_potential(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture,
                                       used_glass_for_furniture, used_plastics_for_furniture):
    steel =  1.836568936 # kg Co2 per tonne
    plastic = 3.451825009 # kg Co2 per tonne

    # keine richtig geile quelle für glas: http://www.greenrationbook.org.uk/resources/footprints-glass/
    glass = 4 # kg Co2 per tonne

    wood = 0.28363 # kg Co2 per tonne

    # quelle für aluminium:
    aluminium = 8.14 # kg Co2 per tonne

    gwp = used_wood_for_furniture * wood + used_steel_for_furniture * steel + used_aluminium_for_furniture * aluminium + used_plastics_for_furniture * plastic + used_glass_for_furniture * glass

    return gwp


def calculate_emission2():
    pass


def calculate_emission3():
    pass


def create_price_subplots(data_dic):

    fig, ax = plt.subplots(8, figsize=(22,22))
    # fig.suptitle('Overview Prices')
    fig.tight_layout(pad=3.0)
    # plt.grid(color='b', linestyle='-', linewidth=0.1)
    ax[0].plot(data_dic["value_time"], data_dic["value_megatrends"])
    ax[0].set_title("megatrends")
    ax[1].plot(data_dic["value_time"], data_dic["value_index"])
    ax[1].set_title("index")
    ax[2].plot(data_dic["value_time"], data_dic["value_pro_environmental_policies"])
    ax[2].set_title("pro_environmental_policies")
    ax[3].plot(data_dic["value_time"], data_dic["value_price_of_wood"])
    ax[3].set_title("value_price_of_wood (€)")
    ax[4].plot(data_dic["value_time"], data_dic["value_price_of_steel"])
    ax[4].set_title("value_price_of_steel (€)")
    ax[5].plot(data_dic["value_time"], data_dic["value_price_of_aluminium"])
    ax[5].set_title("value_price_of_aluminium (€)")
    ax[6].plot(data_dic["value_time"], data_dic["value_price_of_glass"])
    ax[6].set_title("value_price_of_glass (€)")
    ax[7].plot(data_dic["value_time"], data_dic["value_price_of_plastics"])
    ax[7].set_title("value_price_of_plastics (€)")
    for i in range(8):
        ax[i].grid()
    plt.savefig("static/overview_prices")
    plt.close()
    plt.show()


def create_material_supply_subplot(data_dic):
    fig, ax = plt.subplots(8, figsize=(22,22))
    # fig.suptitle('Current Material Supplies')
    fig.tight_layout(pad=3.0)
    # plt.grid(color='b', linestyle='-', linewidth=0.1)
    ax[0].plot(data_dic["value_time"], data_dic["value_megatrends"])
    ax[0].set_title("megatrends")
    ax[1].plot(data_dic["value_time"], data_dic["value_index"])
    ax[1].set_title("index")
    ax[2].plot(data_dic["value_time"], data_dic["value_pro_environmental_policies"])
    ax[2].set_title("pro_environmental_policies")
    ax[3].plot(data_dic["value_time"], data_dic["value_current_supply_of_wood"])
    ax[3].set_title("value_current_supply_of_wood (tons)")
    ax[4].plot(data_dic["value_time"], data_dic["value_current_supply_of_steel"])
    ax[4].set_title("value_current_supply_of_steel (tons)")
    ax[5].plot(data_dic["value_time"], data_dic["value_current_supply_of_aluminium"])
    ax[5].set_title("value_current_supply_of_aluminium (tons)")
    ax[6].plot(data_dic["value_time"], data_dic["value_current_supply_of_glass"])
    ax[6].set_title("value_current_supply_of_glass (tons)")
    ax[7].plot(data_dic["value_time"], data_dic["value_current_supply_of_plastics"])
    ax[7].set_title("value_current_supply_of_plastics (tons)")
    for i in range(8):
        ax[i].grid()
    plt.savefig("static/current_material_supplies")
    plt.close()
    plt.show()


def create_used_materials_and_emissions_subplots(data_dic):

    fig, ax = plt.subplots(9, figsize=(22,22))
    # fig.suptitle('Used Materials + Emissions')
    fig.tight_layout(pad=3.0)
    # plt.grid(color='b', linestyle='-', linewidth=0.1)
    ax[0].plot(data_dic["value_time"], data_dic["value_megatrends"])
    ax[0].set_title("megatrends")
    ax[1].plot(data_dic["value_time"], data_dic["value_index"])
    ax[1].set_title("index")
    ax[2].plot(data_dic["value_time"], data_dic["value_pro_environmental_policies"])
    ax[2].set_title("pro_environmental_policies")
    ax[3].plot(data_dic["value_time"], data_dic["value_used_wood_for_furniture"])
    ax[3].set_title("value_used_wood_for_furniture (tons)")
    ax[4].plot(data_dic["value_time"], data_dic["value_used_steel_for_furniture"])
    ax[4].set_title("value_used_steel_for_furniture (tons)")
    ax[5].plot(data_dic["value_time"], data_dic["value_used_aluminium_for_furniture"])
    ax[5].set_title("value_used_aluminium_for_furniture (tons)")
    ax[6].plot(data_dic["value_time"], data_dic["value_used_glass_for_furniture"])
    ax[6].set_title("value_used_glass_for_furniture (tons)")
    ax[7].plot(data_dic["value_time"], data_dic["value_used_plastics_for_furniture"])
    ax[7].set_title("value_used_plastics_for_furniture (tons)")
    ax[8].plot(data_dic["value_time"], data_dic["value_gwp"])
    ax[8].set_title("KG CO2 eq. emitted (per year)")
    for i in range(9):
        ax[i].grid()
    plt.savefig("static/used_materials_and_emissions")
    plt.close()
    plt.show()


def run(counter):
    # setup initial variables
    # dv = decimal values
    dv = 2
    megatrends = initial_megatrend
    current_supply_of_wood = initial_amount_of_wood
    current_supply_of_steel = initial_supply_of_steel
    current_supply_of_aluminium = initial_supply_of_aluminium
    current_supply_of_glass = initial_supply_of_glass
    current_supply_of_plastics = initial_supply_of_plastics

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


    for year in range(counter):
        print(f"Run: {year} "+ " / Year: " + str(2022 + year))

        pro_environmental_policies, election_results = calculate_pro_environmental_policies(megatrends, year, election_results)

        current_supply_of_wood = calculate_supply_of_wood(pro_environmental_policies, growth_rate, current_supply_of_wood)

        price_of_wood = calculate_price_of_wood_m(initial_price_of_wood, current_supply_of_wood, initial_amount_of_wood)

        current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics = calculate_supply_of_non_wood_m(pro_environmental_policies, current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics, growth_rate_2)

        price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics, ratio_steel = calculate_price_of_non_wood_m(initial_price_of_wood, price_of_wood, initial_price_steel, current_supply_of_steel, initial_supply_of_steel, initial_price_aluminium, current_supply_of_aluminium, initial_supply_of_aluminium, initial_price_glass, current_supply_of_glass, initial_supply_of_glass, initial_price_plastics, current_supply_of_plastics, initial_supply_of_plastics)

        ratio_for_wood_furniture_demand = calculate_demand_for_furniture(megatrends)

        used_wood_for_furniture = calculate_stock_amount_of_wood_material(industry_wood_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood, ratio_steel)

        used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture = calculate_stock_amount_of_non_wood_material(initial_price_steel, price_of_steel,industry_steel_demand,initial_price_aluminium, price_of_aluminium, industry_aluminium_demand,initial_price_glass, price_of_glass, industry_glass_demand,initial_price_plastics, price_of_plastics, industry_placstics_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood)

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

    data_dic = {"value_time": value_time,
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
                "value_gwp": value_gwp
                }

    return data_dic


if __name__ == "__main__":

    print("\nSystem message: Creating Data Dict ...\n")
    data_dic = run(10)
    print(colored("\nSystem message: Data Dict created!\n", "green"))

    print("\nSystem message: Creating plots ...\n")
    create_price_subplots(data_dic)
    create_material_supply_subplot(data_dic)
    create_used_materials_and_emissions_subplots(data_dic)
    print(colored("\nSystem message: Plots created and saved!\n", "green"))

    # print("Values in Data dict:")
    # for key, value in data_dic.items():
    #     print('%s,%s\n' % (key, value))

    print("\nSystem message: Creating Simulation Dataframe ...\n")
    df = pd.DataFrame(data_dic, dtype=float)
    df.to_csv(r"static\simulation.csv", index=False, sep=";")
    print(colored("\nSystem message: Simulation Dataframe created and saved!\n", "green"))

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(colored("\nSystem message: Dataframe head:", "green"))
    print(df.head())

