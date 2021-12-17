import json
from datetime import date
from datetime import datetime

years = 5
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
data_file_name = "Simulation_" + dt_string

data_dict = {"Runs": years, "Data and Time of Simulation": dt_string}

with open(f'{data_file_name}.csv', 'w') as file:
    for key, value in data_dict.items():
        file.write('%s,%s\n' % (key, value))