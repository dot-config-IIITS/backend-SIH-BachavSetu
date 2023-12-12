from flask_socketio import Namespace, emit
from flask import request 

from Functions.functions import send_otp, gen_otp, gen_token

from config import mongo_uri
from Database.client_database import client_database, client_post

client_db = client_database(mongo_uri=mongo_uri)

class client_routes(Namespace) :
    def on_connect(self):
        print("hell yeah")

    def on_disconnect(self) :
        client_post.pop(request.sid)

    def on_verify_token(self, data) :
        token = data['token']
        phone = data['phone']
        emit('verify_token_result', client_db.verify_token(token=token, phone=phone, sid=request.sid) , to=request.sid)

    def on_get_otp(self, data):
        phone = data['phone']
        otp = gen_otp()
        client_post.phone_otp_pair[phone] = otp 
        print(phone, client_post.phone_otp_pair[phone])
        # send_otp(phone=phone, otp=otp)
    
    def on_verify_otp(self, data) :
        phone = data['phone']
        otp = data['otp']
        if (phone in client_post.phone_otp_pair) :
            if (client_post.phone_otp_pair[phone] == otp) :
                token = gen_token()
                user = client_db.find_user(phone=phone)

                # Binding the request sid to the phone no
                client_post.sid_phone_pair[request.sid] = phone 

                if (user) :
                    client_db.update_token(phone=phone, token=token)
                    if (user['name'] == '') :
                        emit ('verify_otp_result',{'status':'details_not_filled','token':token}, to=request.sid)
                    else :
                        emit_data = {'status':'details_filled','token':token ,
                                     'name':user['name'], 'blood_group':user['blood_group'], 'emergency_contact':user['emergency_contact'],
                                     'relation':user['relation'], 'age':user['age'], 'gender':user['gender']}
                        emit ('verify_otp_result',emit_data, to=request.sid)
                else :
                    client_db.add_user(phone=phone,token=token)
                    emit ('verify_otp_result',{'status':'details_not_filled', 'token':token}, to=request.sid)
            else :
                emit('verify_otp_result', {'status':'Wrong OTP'} , to=request.sid)  
        else :
            emit('verify_otp_result', {'status':'No OTP is sent to this phone no.'} , to=request.sid)  

    def on_add_details(self, data) :
        sid = request.sid 
        if (sid in client_post.sid_phone_pair) :
            name = data['name']
            age = data['age']
            blood_group = data['blood_group']
            emergency_contact = data['emergency_contact']
            gender = data['gender']
            relation = data['relation']
            if (name and age and blood_group and emergency_contact and relation) :
                client_db.add_details(phone = client_post.sid_phone_pair[sid], name = name, blood_group = blood_group, 
                                      gender = gender, emergency_contact = emergency_contact, relation = relation, age=age)
                emit('add_details_result',{'status':'success'})
            else :
                emit('add_details_result',{'status':'One of the fields is empty'}, to=request.sid)

        else :
            emit('add_details_result',{'status':'token not verified'}, to=request.sid)
        
# if (token exists) :
#     try connecting to server with the token 
#     if (status != 'auth_fail') :
#         if (status == 'details_filled') : 
#                 Load the remaining stuff
#         else :
#             ask for details 
#             send details..
#     else : 
#         ask user to enter phone to login
# else :
#     ask user to enter phone to login 
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

