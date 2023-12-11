from random import randint
from twilio.rest import Client 
from string import ascii_letters, digits
from secrets import choice
from config import twilio_account_sid, twilio_auth_token
otp_client = Client(twilio_account_sid,twilio_auth_token)

def gen_otp():
    return str(randint(100000,999999))

def send_otp(otp, phone):
    otp_client.messages.create(
        body = "Your OTP : "+otp+" \nExpirese within 5 minutes",
        from_ = "+13478686688",
        to = "+91"+phone)
    
def gen_token(token_length = 128):  
    return ''.join(choice(ascii_letters + digits) for _ in range(token_length))