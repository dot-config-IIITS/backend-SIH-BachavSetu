from json import load 
file_name = 'states_districts.json'
with open(file_name) as file :
    data1 = load(file)

file_name = 'states_codes.json'
with open (file_name) as file :
    data2 = load(file)
