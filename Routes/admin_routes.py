from flask_socketio import Namespace, emit
from flask import request 
from Database.admin_database import admin_cache, admin_database
from Database.rescue_database import rescue_cache
from asyncio import sleep
# from ..app import admin_db

class admin_routes(Namespace) :

    def on_connect(self):
        sid = request.sid
        pass 

    def on_disconnect(self) :
        sid = request.sid
        admin_cache.ssd_pair.pop(sid)

    def on_login(self, data) :
        state = data['state']
        district = data['district']
        password = data['password']
        sid = request.sid
        login_result = admin_database.login(state = state, password = password, district = district, sid=sid)
        if (login_result['status'=='success']):
            admin_cache.ssd_pair[sid] = {'state':state, 'district':district}
        emit('login_result', login_result)

    def on_verify_token(self, data) :
        sid = request.sid
        state = data['state']
        district = data['district']
        token = data['token']
        token_verified = admin_database.verify_token(token = token, district = district, state = state)
        if (token_verified['status'] == 'success') :
            admin_cache.ssd_pair[sid] = {'state':state, 'district':district}
        emit('verify_token_result',token_verified)


    # def on_list_teams(self):
    #     sid = request.sid 
    #     state_district = admin_cache.ssd_pair.get(sid, None)
    #     if (state_district):
    #         state = state_district['state']
    #         district = state_district['district']
    #         # rescue_teams = rescue_database.list_teams(state=state, district=district)
    #         admin_database.add_rescue_team(state=state, district=district)
    #     else :
    #         emit('get_teams_result',{'status':'verify token first'})
        


    # def on_fake_case(self) :

    # def on_dispatch_team(self) :

    # def on_mark_case_as_complete(self):

    # def on_add_site(self)

    # def on_a 

    def on_add_rescue_team(self, data) :
        sid = request.sid 
        state_district = admin_cache.ssd_pair.get(sid, None)
        if (state_district):
            state = state_district['state']
            district = state_district['district']
            phone = data['phone']
            type = data['type']
            admin_database.add_rescue_team(state=state, district=district, phone=phone, type=type)
        else :
            emit('add_rescue_team_result',{'status':'verify token first'})

    # def on_update_radius(self, data):
    #     sid = request.sid
    #     admin_cache.ssd_pair[]

    
def notify_danger_site(coordinates, state, district, type) :
    for sid in admin_cache.ssd_pair :
        state_district = admin_cache.ssd_pair[sid] 
        sid_state = state_district['state']
        sid_district = state_district['district']
        if (state == sid_state and district == sid_district) :
            emit("notify_danger_site",{"coordinates":coordinates, "type":type}, to=sid)
            break

async def update_coordinates(socketio):
    sleep(5)
    for sid, state_district in admin_cache.ssd_pair.items() :
        state = state_district['state']
        district = state_district['district']
        room = state+"_"+district
        if (room in rescue_cache.sd_rooms) :
            rescue_sids = socketio.rooms.get(room, set())
            for rescue_sid in rescue_sids :
                rescue = rescue_cache.spsdc_pair[rescue_sid] 
                coordinates = rescue['coordinates']
                

        

# """
# This is Hruthik from team .config, IIIT Sriciry.
# I am thrilled and elated to be a participant in the finals of the Smart India Hackathon.
# My team chose the problem statement disaster management and is diligently working on a system that fundamentally streamlines the process of disaster management.
# I am helping my team with the backend and server deployment.
# Despite encountering challenges during the development process, I am confident that my team will emerge victorious.
# """