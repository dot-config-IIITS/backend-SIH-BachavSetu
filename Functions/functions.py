from random import randint
from requests import request
from string import ascii_letters, digits
from secrets import choice
from config import otp_api_key

def gen_otp():
    return str(randint(100000,999999))

def send_otp(otp, phone):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    querystring = {"authorization":otp_api_key,"variables_values":otp,"route":"otp","numbers":phone}
    headers = {'cache-control': "no-cache"}
    response = request("GET", url, headers=headers, params=querystring)
    print(response.text)
    
def gen_token(token_length = 128):  
    return ''.join(choice(ascii_letters + digits) for _ in range(token_length))