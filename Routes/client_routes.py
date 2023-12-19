from flask_socketio import Namespace, emit
from flask import request 
from os.path import exists 
from os import makedirs

from config import system_states, logger
from Functions.functions import send_otp, gen_otp, gen_token, gen_file_name
from Database.client_database import client_database, client_pos
from Database.report_database import report_database
# from Routes.admin_routes import notify_danger_site

# Could be optimized by asking for state, district, phone, token (make this requests..) 
# Creating a client database, putting collections as state_district
# Index documents with phone number 
# Problem :- gotta look through all the documents in all the collections in the mongodb
#            to check if the user registered with some other state and district 
# Solution :- Webscrape https://tathya.uidai.gov.in/login and verify users via aadhar
#             get their state, district from aadhar details..
#             Now user cannot choose his/her state/district, these details are extracted from aadhar details..
#             They just have to add blood_group now..
# Don't have enough time for optimizations rn 😞

# Gotta test searching for an indexed document in 18 Lakh documents (local as well as cloud)

class client_routes(Namespace) :

    def on_logout(self) : 
        sid = request.sid
        if (sid in client_pos.sid_phone_pair) :
            phone = client_pos.sid_phone_pair[sid]
            client_database.update_token(phone=phone, token='')
            client_pos.sid_phone_pair.pop(request.sid)
            emit('logout_result',{'status':'success'}, to=sid)
        else :
            emit('logout_result', {'status':'Verify token first'}, to=sid)

    def on_submit_feedback(self, data) :
        sid = request.sid
        if (sid in client_pos.sid_phone_pair) :
            phone = client_pos.sid_phone_pair[sid]
            emit ('submit_feedback_result',client_database.submit_feedback(phone = phone, feedback = data['feedback'],
                                                                     state = data['state'], district = data['district']))
        else :
            emit ('submit_feedback_result',{'status':'Verify token first'})

    def on_connect(self):
        logger.warning("Client name space connected")

    def on_disconnect(self) :
        sid = request.sid
        if (sid in client_pos.sid_phone_pair):
            client_pos.sid_phone_pair.pop(sid)

    def on_verify_token(self, data) :
        token = data['token']
        phone = data['phone']
        emit('verify_token_result', client_database.verify_token(token=token, phone=phone, sid=request.sid) , to=request.sid)

    def on_get_otp(self, data):
        phone = data['phone']
        otp = gen_otp()
        client_pos.phone_otp_pair[phone] = otp 
        
        if (system_states.SEND_OTP == None) :
            # send_otp(phone=phone, otp=otp)
            logger.warning('Phone : '+phone+' | OTP : '+otp)

        elif (system_states.SEND_OTP == 'TRUE') :
            send_otp(phone=phone, otp=otp)
        else:
            logger.warning('Phone : '+phone+' | OTP : '+otp)
    
    def on_verify_otp(self, data) :
        phone = data['phone']
        otp = data['otp']
        sid = request.sid
        if (phone in client_pos.phone_otp_pair) :
            if (client_pos.phone_otp_pair[phone] == otp) :
                token = gen_token()
                user = client_database.find_client(phone=phone)

                # Binding the request sid to the phone no                 
                client_pos.sid_phone_pair[sid] = phone

                if (user) :
                    client_database.update_token(phone=phone, token=token)
                    if (user['name'] == '') :
                        emit ('verify_otp_result',{'status':'details_not_filled','token':token}, to=sid)
                    else :
                        emit_data = {'status':'details_filled','token':token ,
                                     'name':user['name'], 'blood_group':user['blood_group'], 'emergency_contact':user['emergency_contact'],
                                     'relation':user['relation'], 'dob':user['dob'], 'gender':user['gender']}
                        emit ('verify_otp_result',emit_data, to=sid)
                else :
                    client_database.add_client(phone=phone,token=token, sid=sid)
                    emit ('verify_otp_result',{'status':'details_not_filled', 'token':token}, to=sid)
            else :
                emit('verify_otp_result', {'status':'Wrong OTP'} , to=sid)  
        else :
            emit('verify_otp_result', {'status':'No OTP is sent to this phone no.'} , to=sid)  

    def on_add_details(self, data) :
        sid = request.sid 
        if (sid in client_pos.sid_phone_pair) :
            name = data['name']
            dob = data['dob']
            blood_group = data['blood_group']
            emergency_contact = data['emergency_contact']
            gender = data['gender']
            relation = data['relation']
            if (name and dob and blood_group and emergency_contact and relation) :
                client_database.add_details(phone = client_pos.sid_phone_pair[sid], name = name, blood_group = blood_group, 
                                      gender = gender, emergency_contact = emergency_contact, relation = relation, dob=dob)
                emit('add_details_result',{'status':'success'})
            else :
                emit('add_details_result',{'status':'One of the fields is empty'}, to=request.sid)

        else :
            emit('add_details_result',{'status':'token not verified'}, to=request.sid)

    def on_report_danger_site(self, data) :
        sid = request.sid 
        if (sid in client_pos.sid_phone_pair):
            phone = client_pos.sid_phone_pair[sid]
            
            file_data = data['file_data']
            coordinates = data['coordinates']
            type = data['type']
            state = data['state']
            district = data['district']
            text = data['text']

            file_name = gen_file_name(phone=phone)
            with open (file_name, 'wb') as file :
                file.write(file_data)
            report_id = report_database.add_report(phone=phone, coordinates=coordinates, type=type, file_name=file_name, text=text)
            client_database.db.update_one({'phone':phone}, {'$push',{'report_ids':report_id}})
            # notify_danger_site(coordinates = coordinates, state= state, district = district, type = type, phone=phone, report_id = report_id)

        else :
            emit('report_danger_site_result',{'status' : 'Verify token first'})


### Reports folder ..
# All report-files, file name : id_time

### reports collection
# file-name, user id, coordinates, type

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

# 1. User Profile (Load at starting of the app)
# 2. Submit disaster 
# photo, video, description
# 3. Send Feedback
# 4. Logout route


# Local  : 
#     addr for VM      : 'http://10.0.2.2:5000/client'
#     addr for phycial : 'http://laptops_ip_add:5000/client'
#     (for physical + local, laptop, phone have to be on same network)

# Cloud  :
#     addr for VM, physical : 'http://bachavsetu.onrender.com/client'
#                              Its is .com/client and not .com:5000/client