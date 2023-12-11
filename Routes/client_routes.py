from flask_socketio import Namespace, emit
from flask import request 

from Functions.functions import send_otp, gen_otp

from config import mongo_uri
from Database.client_database import client_database
client_db = client_database(mongo_uri=mongo_uri)

class client_routes(Namespace) :
    def on_disconnect(self) :
        sid = request.sid
        pass 

    def on_verify_token(self, data) :
        token = data['token']
        phone_no = data['phone_no']
        emit('verify_token_result', client_db.verify_token(token=token, phone_no=phone_no) , to=request.sid)
        
# if (token exists) :
#     try connecting to server with the token 
#     if (status != 'auth_fail') :
#         if (status == 'details_filled') : 
#                 Load the remaining stuff
#         else :
#             ask for details 
#             send details..
#     else : 
#         ask user to enter phone_no to login
# else :
#     ask user to enter phone_no to login 
#     enter otp
#     if (status != 'auth_fail'): 
#         save token in local storage (you would get the token in the response 
#                                     when you send the otp along with the status)
#         if (status == 'details_filled'):
#             load the remaining stuff
#         else :
#             ask for details 
#             send details..
#     else :
#         wrong_otp..

