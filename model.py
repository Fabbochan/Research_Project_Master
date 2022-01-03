# import json
import random
import matplotlib.pyplot as plt


# TODO: make it so variables can be loaded in from an input data file
# Global Initial Variables
growth_rate = 1.03 # dmnl - for supply of wood market
growth_rate_2 = 1.02  # dmnl - for supply of non wodden materials market

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

# variable
material_trends = True

# Initial seed
# seed = 10


def calculate_megatrend(index, megatrends):

    value_megatrends = megatrends * ((index/100) + 1)
    return value_megatrends


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
    price_of_wood = ((initial_price_of_wood) / (current_supply_of_wood / initial_amount_of_wood))
    return price_of_wood


def calculate_price_of_non_wood_m(initial_price_of_wood, price_of_wood, initial_price_steel, current_supply_of_steel, initial_supply_of_steel, initial_price_aluminium, current_supply_of_aluminium, initial_supply_of_aluminium, initial_price_glass, current_supply_of_glass, initial_supply_of_glass, initial_price_plastics, current_supply_of_plastics, initial_supply_of_plastics):

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

    if material_trends:
        material_trends_variable = 0 + random.uniform(-0.1, 0.1)
    else:
        material_trends_variable = 0

    if megatrends >= 50:
        demand_for_furniture = (megatrends / 1000 + 1) + material_trends_variable
    else:
        demand_for_furniture = (1 - (megatrends / 1000)) + material_trends_variable
    print("demand_for_furniture")
    print(demand_for_furniture)
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


def calculate_stock_amount_of_wood_material(industry_wood_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood, ratio_steel):

    used_wood_for_furniture = (industry_wood_demand / (price_of_wood / initial_price_of_wood) * ratio_for_wood_furniture_demand) * ratio_steel
    return used_wood_for_furniture


def calculate_stock_amount_of_non_wood_material(initial_price_steel, price_of_steel,industry_steel_demand,initial_price_aluminium, price_of_aluminium, industry_aluminium_demand,initial_price_glass, price_of_glass, industry_glass_demand,initial_price_plastics, price_of_plastics, industry_placstics_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood):

    ratio_wood_price = price_of_wood/initial_price_of_wood

    # TODO price of wood
    used_steel_for_furniture = (industry_steel_demand / (price_of_steel / initial_price_steel) / ratio_for_wood_furniture_demand) * ratio_wood_price
    used_aluminium_for_furniture = (industry_aluminium_demand / (price_of_aluminium / initial_price_aluminium) / ratio_for_wood_furniture_demand) * ratio_wood_price
    used_glass_for_furniture = (industry_glass_demand / (price_of_glass / initial_price_glass) / ratio_for_wood_furniture_demand) * ratio_wood_price
    used_plastics_for_furniture = (industry_placstics_demand / (price_of_plastics / initial_price_plastics) / ratio_for_wood_furniture_demand) * ratio_wood_price

    return used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture


def calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture):

    sum_used_wood = used_wood_for_furniture
    sum_non_wood = used_steel_for_furniture + used_aluminium_for_furniture + used_glass_for_furniture + used_plastics_for_furniture
    return sum_used_wood / (sum_used_wood + sum_non_wood)


def calculate_global_warming_potential(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture):
    steel =  1.836568936 # per tonne
    plastic = 3.451825009 # per tonne

    # keine richtig geile quelle für glas: http://www.greenrationbook.org.uk/resources/footprints-glass/
    glass = 4 # per tonne

    wood = 0.28363 # per tonne

    # quelle für aluminium:
    aluminium = 8.14

    gwp = used_wood_for_furniture * wood + used_steel_for_furniture * steel + used_aluminium_for_furniture * aluminium + used_plastics_for_furniture * plastic + used_glass_for_furniture * glass

    return gwp


def calculate_emission2():
    pass


def calculate_emission3():
    pass


def create_price_subplots(data_dic):

    fig, ax = plt.subplots(8, figsize=(15,15))
    # fig.suptitle('Overview Prices')
    fig.tight_layout()
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
        ax[i].grid(b=True, which='major', color='#666666', linestyle='-')
    plt.savefig("static/overview_prices")
    plt.close()
    plt.show()


def create_material_supply_subplot(data_dic):
    fig, ax = plt.subplots(8, figsize=(15,15))
    # fig.suptitle('Current Material Supplies')
    fig.tight_layout()
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
        ax[i].grid(b=True, which='major', color='#666666', linestyle='-')
    plt.savefig("static/current_material_supplies")
    plt.close()
    plt.show()


def create_used_materials_and_emissions_subplots(data_dic):

    fig, ax = plt.subplots(9, figsize=(15,15))
    # fig.suptitle('Used Materials + Emissions')
    fig.tight_layout()
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
    ax[8].set_title("KG CO2 eq. emitted per year")
    for i in range(9):
        ax[i].grid(b=True, which='major', color='#666666', linestyle='-')
    plt.savefig("static/used_materials_and_emissions")
    plt.close()
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


    for year in range(counter):
        print("______________________")
        print("Year (run): " + str(year + 1))

        pro_environmental_policies = calculate_pro_environmental_policies(megatrends)
        # print(f"\nPro_environmental_policies: {pro_environmental_policies} dmnl\n")

        current_supply_of_wood = calculate_supply_of_wood(pro_environmental_policies, growth_rate, current_supply_of_wood)
        # print(f"Current_supply_of_wood: {current_supply_of_wood} tons\n")

        price_of_wood = calculate_price_of_wood_m(initial_price_of_wood, current_supply_of_wood, initial_amount_of_wood)
        # print(f"Price_of_wood: {price_of_wood} €\n")

        current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics = calculate_supply_of_non_wood_m(pro_environmental_policies, current_supply_of_steel, current_supply_of_aluminium, current_supply_of_glass, current_supply_of_plastics, growth_rate_2)
        # print(f"Current_supply_of_steel: {current_supply_of_steel} tons\nCurrent_supply_of_aluminium: {current_supply_of_aluminium} tons\nCurrent_supply_of_glass: {current_supply_of_glass} tons\nCurrent_supply_of_plastics: {current_supply_of_plastics} tons\n")

        price_of_steel, price_of_aluminium, price_of_glass, price_of_plastics, ratio_steel = calculate_price_of_non_wood_m(initial_price_of_wood, price_of_wood, initial_price_steel, current_supply_of_steel, initial_supply_of_steel, initial_price_aluminium, current_supply_of_aluminium, initial_supply_of_aluminium, initial_price_glass, current_supply_of_glass, initial_supply_of_glass, initial_price_plastics, current_supply_of_plastics, initial_supply_of_plastics)
        # print(f"price_of_steel: {price_of_steel} €\nPrice_of_aluminium: {price_of_aluminium} €\nPrice_of_glass: {price_of_glass} €\nPrice_of_plastics: {price_of_plastics} €\n")

        ratio_for_wood_furniture_demand = calculate_demand_for_furniture(megatrends)
        # print(f"| Note: If demand is @ 1.0 - default demand is displayed - if demand increases - more wood furniture is demanded by the market |\nratio_for_wood_furniture_demand: {ratio_for_wood_furniture_demand} dmnl\n")

        used_wood_for_furniture = calculate_stock_amount_of_wood_material(industry_wood_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood, ratio_steel)
        # print(f"used_wood_for_furniture: {used_wood_for_furniture} tons\n")

        used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture = calculate_stock_amount_of_non_wood_material(initial_price_steel, price_of_steel,industry_steel_demand,initial_price_aluminium, price_of_aluminium, industry_aluminium_demand,initial_price_glass, price_of_glass, industry_glass_demand,initial_price_plastics, price_of_plastics, industry_placstics_demand, price_of_wood, ratio_for_wood_furniture_demand, initial_price_of_wood)
        # print(f"Used_steel_for_furniture: {used_steel_for_furniture} tons\nUsed_aluminium_for_furniture: {used_aluminium_for_furniture} tons\nUsed_glass_for_furniture: {used_glass_for_furniture} tons\nUsed_plastics_for_furniture: {used_plastics_for_furniture} tons")

        index = calculate_index(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture)
        # print(f"\nindex: {index} %")

        megatrends = calculate_megatrend(index, megatrends)
        # print(f"\nmegatrends: {megatrends}")

        gwp = calculate_global_warming_potential(used_wood_for_furniture, used_steel_for_furniture, used_aluminium_for_furniture, used_glass_for_furniture, used_plastics_for_furniture)
        gwp = round(gwp, dv)
        # print(f"\nKg C02 eq: {gwp}")
        print("______________________")

        value_time.append(year + 1)
        value_price_of_wood.append(round(price_of_wood,dv))
        value_index.append(round(index,dv))
        value_pro_environmental_policies.append(round(pro_environmental_policies, dv))
        value_megatrends.append(round(megatrends,dv))
        value_price_of_steel.append(round(price_of_steel,dv))
        value_price_of_aluminium.append(round(price_of_aluminium,dv))
        value_price_of_glass.append(round(price_of_glass,dv))
        value_price_of_plastics.append(round(price_of_plastics,dv))
        value_current_supply_of_wood.append(round(current_supply_of_wood, dv))
        value_current_supply_of_steel.append(round(current_supply_of_steel, dv))
        value_current_supply_of_aluminium.append(round(current_supply_of_aluminium, dv))
        value_current_supply_of_glass.append(round(current_supply_of_glass, dv))
        value_current_supply_of_plastics.append(round(current_supply_of_plastics, dv))
        value_used_wood_for_furniture.append(round(used_wood_for_furniture,dv))
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

    data_dic = run(5)

    create_price_subplots(data_dic)
    create_material_supply_subplot(data_dic)
    create_used_materials_and_emissions_subplots(data_dic)
    print("\nPlots created and saved.")


    for key, value in data_dic.items():
        print('%s,%s\n' % (key, value))

    # with open("data.csv", "w") as f:
    #         f.write(json.dumps(data_dic))

