from flask_socketio import Namespace, emit
from flask import request 

from config import mongo_uri
from Database.rescue_database import rescue_database, rescue_post


from Functions.functions import send_otp, gen_otp, gen_token

rescue_db = rescue_database(mongo_uri=mongo_uri)

class rescue_routes(Namespace) :
    def on_disconnect(self) :
        rescue_post.pop(request.sid)
    
    def on_get_otp(self, data):
        phone = data['phone']
        if (rescue_db.find_user(phone=phone)):
            otp = gen_otp()
            rescue_post.phone_otp_pair[phone] = otp 
            print(phone, rescue_post.phone_otp_pair[phone])
            #send_otp(phone=phone, otp=otp)
        else :
            emit('get_otp_result',{'status':'No Rescue account registered with this phone no.'}, to=request.sid)

    def on_verify_otp(self, data) :
        phone = data['phone']
        otp = data['otp']
        if (phone in rescue_post.phone_otp_pair) :
            if (rescue_post.phone_otp_pair[phone] == otp) :
                token = gen_token()
                rescue_db.update_token(phone=phone, token=token)

                # binding the request sid to the phone no
                rescue_post.sid_phone_pair[request.sid] = phone 
                emit ('verify_otp_result',{'status':'success','token':token}, to=request.sid)
            else :
                emit('verify_otp_result', {'status':'Wrong OTP'} , to=request.sid)  
        else :
            emit('verify_otp_result', {'status':'No OTP is sent to this phone no.'} , to=request.sid)     

    def on_verify_token(self, data):
        token = data['token']
        phone = data['phone']
        emit('verify_token_result', rescue_db.verify_token(token=token, phone=phone, sid=request.sid))

    
    # def on_connect(self):
    #     ssid = request.sid
    #     pass 

    # def on_disconnect(self) :
    #     ssid = request.ssid
    #     pass 