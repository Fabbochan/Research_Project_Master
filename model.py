import json
import random
# import matplotlib.pyplot as plt
# import seaborn as sns


# TODO: make it so variables can be loaded in from an input data file
# Global Initial Variables
growth_rate = 1  # dmnl
growth_rate_2 = 1  # dmnl

initial_megatrend = 50  # dmnl
# the higher the megatrend, the higher environmental policies, the cheaper the price of wood

initial_amount_of_wood = 16790000  # tons
industry_wood_demand = 132593  # tons

ratio_metals = 33805  # ratio is 80% aluminium and 20% steel
industry_steel_demand = ratio_metals * 0.2  # tons
industry_aluminium_demand = ratio_metals * 0.8  # tons
# caclculated: gütereinsatzstatistik / preis
industry_glass_demand = 6890  # tons
industry_placstics_demand = 45715  # tons

# Initial Supplies
# 7.4 millionen tons get manifactured each year in austria
initial_supply_of_steel = 7400000  # tons
# ratio supply_of_steel / 35 for aluminium
initial_supply_of_aluminium = 200000  # tons
# laut WKO Bericht
initial_supply_of_glass = 524000  # tons
# in deutschland 17.9 millionen / 0.1 für Österreich
initial_supply_of_plastics = 1790000  # tons

# Initial Prices
initial_price_of_wood = 100  # euro
initial_price_steel = 424.16  # euro
initial_price_aluminium = 2529.51  # euro
# Deutschland - Statisitk Gesamtumsatz: 1321 euro pro tonne
# Östrreich - WKO branchenindustry: 1950 euro pro tonne
initial_price_glass = 1975  # euro
initial_price_plastics = 938.67  # euro


def calculate_megatrend(index):
    # TODO inplement random number to vary
    megatrends = (index - 1) * -100
    return megatrends


def calculate_pro_environmental_policies(megatrends):
    # formula for: pro_environmental_policies
    pro_environmental_policies = 0.5 + (megatrends/100)
    return pro_environmental_policies


def calculate_supply_of_wood(pro_environmental_policies, growth_rate, current_supply_of_wood):
    # formula for: current_supply_of_wood
    current_supply_of_wood_return = pro_environmental_policies * growth_rate * current_supply_of_wood
    return current_supply_of_wood_return


def calculate_supply_of_non_wood_m(pro_environmental_policies, current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics, growth_rate_2):
    # formula for: current_supply_non_wood_m

    current_supply_of_steel = growth_rate_2 * current_supply_of_steel / pro_environmental_policies
    current_supply_of_aluminium = growth_rate_2 * current_supply_of_aluminium / pro_environmental_policies
    current_supply_of_glass = growth_rate_2 * current_supply_of_glass / pro_environmental_policies
    current_supply_of_plastics = growth_rate_2 * current_supply_of_plastics / pro_environmental_policies


    return current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics


def calculate_price_of_wood_m(initial_price_of_wood, current_supply_of_wood, initial_amount_of_wood):
    # formula for: price_of_wood
    price_of_wood = (initial_price_of_wood) / (current_supply_of_wood / initial_amount_of_wood)
    return price_of_wood


def calculate_price_of_non_wood_m(initial_price_of_wood, price_of_wood, initial_price_steel, current_supply_of_steel, initial_supply_of_steel, initial_price_aluminium, current_supply_of_aluminium, initial_supply_of_aluminium, initial_price_glass, current_supply_of_glass, initial_supply_of_glass, initial_price_plastics, current_supply_of_plastics, initial_supply_of_plastics):

    ratio = price_of_wood/initial_price_of_wood
    if ratio >= 1:
        ratio -= random.uniform(0, 0.05)
    else:
        ratio += random.uniform(0, 0.05)

    # print("ratio:")
    # print(ratio)

    price_of_steel = ((initial_price_steel) / (current_supply_of_steel/initial_supply_of_steel)) / ratio
    price_of_aluminium = (initial_price_aluminium) / (current_supply_of_aluminium / initial_supply_of_aluminium) / ratio
    price_of_glass = (initial_price_glass) / (current_supply_of_glass / initial_supply_of_glass) / ratio
    price_of_plastics = (initial_price_plastics) / (current_supply_of_plastics / initial_supply_of_plastics) / ratio
    return price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics


def calculate_demand_for_furniture(megatrends):
    # formula for: demand_for_furniture
    demand_for_furniture = 0.5 + (megatrends/100)
    return demand_for_furniture


def calculate_amount_of_wood_supply(pro_environmental_policies, current_stock_wood_supply, growth_rate):
    # formula for: inflow

    inflow = current_stock_wood_supply * pro_environmental_policies * growth_rate
    # formula for: outflow

    outflow = initial_amount_of_wood
    # formula for: current_stock_wood_supply

    current_stock_wood_supply = inflow - outflow
    print(f"Amount_of_wood_stock: inflow: {inflow}, outflow: {outflow} and current_stock_wood_supply: {current_stock_wood_supply}")
    return current_stock_wood_supply


def calculate_consumption_of_wood_f(ratio_c):
    # ratio_c = number between 0 and 1 | 1 = 100 % intense wood consumption

    consumption_more_intense = ratio_c
    consumption_less_intense = 1 - ratio_c
    pass


def calculate_stock_amount_of_wood_material(industry_wood_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood):

    # TODO price non wooden materials
    # formula for: inflow
    used_wood_for_furniture = industry_wood_demand / (price_of_wood / initial_price_of_wood) * ratio_for_wood_furniture_demand
    return used_wood_for_furniture


def calculate_stock_amount_of_non_wood_material(initial_price_steel, price_of_steel,industry_steel_demand,initial_price_aluminium, price_of_aluminium, industry_aluminium_demand,initial_price_glass, price_of_glass, industry_glass_demand,initial_price_plastics, price_of_plastics, industry_placstics_demand, price_of_wood, ratio_for_wood_furniture_demand):

    # TODO price of wood
    used_steel_for_furniture = industry_steel_demand / (price_of_steel / initial_price_steel) / ratio_for_wood_furniture_demand
    used_aluminium_for_furniture = industry_aluminium_demand / (price_of_aluminium / initial_price_aluminium) / ratio_for_wood_furniture_demand
    used_glass_for_furniture = industry_glass_demand / (price_of_glass / initial_price_glass) / ratio_for_wood_furniture_demand
    used_plastics_for_furniture = industry_placstics_demand / (price_of_plastics / initial_price_plastics) / ratio_for_wood_furniture_demand

    return used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture


def calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture):

    sum_used_wood = used_wood_for_furniture
    sum_non_wood = used_steel_for_furniture + used_aluminium_for_furniture + used_glass_for_furniture + used_plastics_for_furniture
    return sum_used_wood / (sum_used_wood + sum_non_wood)


def calculate_emission1():
    pass


def calculate_emission2():
    pass


def calculate_emission3():
    pass


def create_plot(x_value, y_value, x_label, y_label, title):
    x = x_value
    y = y_value
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def create_multiplot(x_value, y_value, z_value, title1, title2):
    x = x_value
    y = y_value
    z = z_value

    fig, ax = plt.subplots(2)
    ax[0].plot(x, y)
    ax[0].set_title(title1)
    ax[1].plot(x, z)
    ax[1].set_title(title2)
    plt.show()


def run(counter):
    # setup initial variables
    # dv = dezimal values
    dv = 2
    megatrends = initial_megatrend
    current_supply_of_wood = initial_amount_of_wood
    current_supply_of_steel = initial_supply_of_steel
    current_supply_of_aluminium = initial_supply_of_aluminium
    current_supply_of_glass = initial_supply_of_glass
    current_supply_of_plastics = initial_supply_of_plastics

    # stored values from the model, so it is easier to plot them
    value_time = []
    value_pro_environmental_policies = []
    value_current_supply_of_wood = []
    value_price_of_wood = []
    value_current_supply_of_steel, value_current_supply_of_aluminium, value_current_supply_of_glass, value_current_supply_of_plastics = [], [], [], []
    value_price_of_steel, value_price_of_aluminium, value_price_of_glass, value_price_of_plastics = [], [], [], []
    value_used_wood_for_furniture = []
    value_index = []


    for year in range(counter):
        print("______________________")
        print("Run (years): " + str(year + 1))

        pro_environmental_policies = calculate_pro_environmental_policies(megatrends)
        print(f"\nPro_environmental_policies: {pro_environmental_policies} dmnl\n")

        current_supply_of_wood = calculate_supply_of_wood(pro_environmental_policies, growth_rate, current_supply_of_wood)
        print(f"Current_supply_of_wood: {current_supply_of_wood} tons\n")

        price_of_wood = calculate_price_of_wood_m(initial_price_of_wood, current_supply_of_wood, initial_amount_of_wood)
        print(f"Price_of_wood: {price_of_wood} €\n")

        current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics = calculate_supply_of_non_wood_m(pro_environmental_policies, current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics, growth_rate_2)
        print(f"Current_supply_of_steel: {current_supply_of_steel} tons\nCurrent_supply_of_aluminium: {current_supply_of_aluminium} tons\nCurrent_supply_of_glass: {current_supply_of_glass} tons\nCurrent_supply_of_plastics: {current_supply_of_plastics} tons\n")

        price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics = calculate_price_of_non_wood_m(initial_price_of_wood, price_of_wood, initial_price_steel, current_supply_of_steel, initial_supply_of_steel, initial_price_aluminium, current_supply_of_aluminium, initial_supply_of_aluminium, initial_price_glass, current_supply_of_glass, initial_supply_of_glass, initial_price_plastics, current_supply_of_plastics, initial_supply_of_plastics)
        print(f"price_of_steel: {price_of_steel} €\nPrice_of_aluminium: {price_of_aluminium} €\nPrice_of_glass: {price_of_glass} €\nPrice_of_plastics: {price_of_plastics} €\n")

        ratio_for_wood_furniture_demand = calculate_demand_for_furniture(megatrends)
        print(f"| Note: If demand is @ 1.0 - default demand is displayed - if demand increases - more wood furniture is demanded by the market |\nratio_for_wood_furniture_demand: {ratio_for_wood_furniture_demand} dmnl\n")

        used_wood_for_furniture = calculate_stock_amount_of_wood_material(industry_wood_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood)
        print(f"used_wood_for_furniture: {used_wood_for_furniture} tons\n")

        used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture = calculate_stock_amount_of_non_wood_material(initial_price_steel, price_of_steel,industry_steel_demand,initial_price_aluminium, price_of_aluminium, industry_aluminium_demand,initial_price_glass, price_of_glass, industry_glass_demand,initial_price_plastics, price_of_plastics, industry_placstics_demand, price_of_wood, ratio_for_wood_furniture_demand)
        print(f"Used_steel_for_furniture: {used_steel_for_furniture} tons\nUsed_aluminium_for_furniture: {used_aluminium_for_furniture} tons\nUsed_glass_for_furniture: {used_glass_for_furniture} tons\nUsed_plastics_for_furniture: {used_plastics_for_furniture} tons")

        index = calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture)
        print(f"\nindex: {index} %")

        megatrends = calculate_megatrend(index)
        print(f"\nmegatrends: {megatrends}")
        print("______________________")

        value_time.append(round(year,dv))
        value_price_of_wood.append(round(price_of_wood,dv))
        value_index.append(round(index,dv))

    data_dic = {"value_time": value_time, "value_price_of_wood": value_price_of_wood, "value_index": value_index}
    # create_multiplot(value_time, value_price_of_wood, value_index, "price of wood", "index")
    return data_dic


if __name__ == "__main__":

    data_dic = run(100)

    with open("data.csv", "w") as f:
            f.write(json.dumps(data_dic))

