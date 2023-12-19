# SECRET URI, DO NOT SHARE, CAN BE USED TO GAIN FULL ACCESS TO THE DATABASE
mongo_uri = 'mongodb+srv://config:9P69890RJtTCy4LC@sih-config-bachavsetu.1vngw8a.mongodb.net/'
otp_api_key = 'jLHunk24gxzMSisYrIdGqpENTUWFyZw7oQmtK0v8bO63hXacf11Gnhe3yQRYP4xv0rLckIH9aSwbfg62'

from logging import getLogger, DEBUG, StreamHandler, Formatter
logger = getLogger(__name__)
logger.setLevel(DEBUG)
handler = StreamHandler()
formatter = Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

type_radius = { 'earthquake':10, 'cyclone' : 5, 'flood' : 10, 'wildfire' : 5,
                'tornado' : 5, 'tsunami' : 10, 'domestic_fires' : 0.1,
                'road_accident' : 0.1, 'land_slides':0.5, 'industrial_accident':1 }

from os import environ
class system_states :
    SEND_OTP = environ.get('SEND_OTP')