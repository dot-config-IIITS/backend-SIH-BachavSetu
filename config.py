# SECRET URI, DO NOT SHARE, CAN BE USED TO GAIN FULL ACCESS TO THE DATABASE
mongo_uri = 'mongodb+srv://config:9P69890RJtTCy4LC@sih-config-bachavsetu.1vngw8a.mongodb.net/'

from enum import Enum
class Type(Enum) :
    ADMIN  = 0
    CLIENT = 1
    RESCUE = 2