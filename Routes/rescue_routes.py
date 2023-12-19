from flask_socketio import Namespace, emit, join_room, rooms
from flask import request 

from config import system_states
from Database.rescue_database import rescue_database, rescue_cache


from Functions.functions import send_otp, gen_otp, gen_token


class rescue_routes(Namespace) :

    def on_disconnect(self) :
        rescue_cache.sid_phone_district_state_pair.pop(request.sid)
    
    def on_get_otp(self, data):
        phone = data['phone']
        district = data['district']
        state = data['state']
        member = rescue_database.find_rescue(phone=phone, district=district, state=state)
        if (member['status'] == "success"):
            otp = gen_otp()
            rescue_cache.phone_otp_pair[phone] = otp 
            if (system_states.SEND_OTP == None) :
                print(phone, rescue_cache.phone_otp_pair[phone])
            else :
                send_otp(phone=phone, otp=otp)
        else :
            emit('get_otp_result',member, to=request.sid)

    def on_verify_otp(self, data) :
        phone = data['phone']
        otp = data['otp']
        state = data['state']
        district = data['district']
        if (phone in rescue_cache.phone_otp_pair) :
            if (rescue_cache.phone_otp_pair[phone] == otp) :
                token = gen_token()
                rescue_database.update_token(phone=phone, token=token)

                # binding the request sid to the phone no, district, state 
                rescue_cache.spsd_pair[request.sid] = {'state':state, 'district':district, 'phone':phone}
                room = state+"_"+district
                if (room in rescue_cache.sd_rooms) :
                    join_room(room)
                else :
                    rescue_cache.sd_rooms.append(room)
                    join_room(room)
                emit ('verify_otp_result',{'status':'success','token':token}, to=request.sid)
            else :
                emit('verify_otp_result', {'status':'Wrong OTP'} , to=request.sid)  
        else :
            emit('verify_otp_result', {'status':'No OTP is sent to this phone no.'} , to=request.sid)     

    def on_verify_token(self, data):
        token = data['token']
        phone = data['phone']
        state = data['state']
        district = data['district']
        token_verified = rescue_database.verify_token(token=token, phone=phone, district=district, state=state)
        if (token_verified['status'] == 'success'):
            room = state+"_"+district
            if (room not in rescue_cache.sd_rooms):
                rescue_cache.sd_rooms.append(room)
            join_room(room)
            emit('verify_token_result',{'status':'success'})
        else :
            emit('verify_token_result', token_verified)


    def on_update_coordinates(self, data):
        sid = request.sid
        if (sid not in rescue_cache.spc_pair) :
            phone_coordinates = rescue_cache.spc_pair[sid]
            coordinates = data['coordinates']
            rescue_cache.spc_pair[sid] = {'coordinates':coordinates, 'phone':phone_coordinates['phone']}
        else :
            emit('update_coordinates_result',{'status':'verify token first'})


    # def on_add_site(self, data) :
    #     coordinates = data['coordinates']



# 597926742059
# CUGPC0055F
    
    # def on_connect(self):
    #     ssid = request.sid
    #     pass 

    # def on_disconnect(self) :
    #     ssid = request.ssid
    #     pass 