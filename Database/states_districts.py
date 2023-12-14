# Extracted from https://igod.gov.in/sg/states

from json import loads 
states_districts = loads(open('Database/states_districts.json','r').read())

def state_district_pair_exists(state, district) :
    for a in states_districts :
        if (states_districts[a]['name'] == state) :
            if (district in states_districts[a]['districts']) :
                return 1
            else :
                return 0
    return 0