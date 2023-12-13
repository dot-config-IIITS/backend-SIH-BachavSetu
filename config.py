# SECRET URI, DO NOT SHARE, CAN BE USED TO GAIN FULL ACCESS TO THE DATABASE
mongo_uri = 'mongodb+srv://config:9P69890RJtTCy4LC@sih-config-bachavsetu.1vngw8a.mongodb.net/'
otp_api_key = 'jLHunk24gxzMSisYrIdGqpENTUWFyZw7oQmtK0v8bO63hXacf11Gnhe3yQRYP4xv0rLckIH9aSwbfg62'

from os import environ
class States :
    def __init__(self) -> None:
        self.SEND_OTP = environ.get('SEND_OTP')

system_states = States()