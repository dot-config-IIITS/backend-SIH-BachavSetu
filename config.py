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

from os import environ
class system_states :
    SEND_OTP = environ.get('SEND_OTP')