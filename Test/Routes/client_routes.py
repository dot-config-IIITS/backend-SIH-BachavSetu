from socketio import ClientNamespace

class client_routes(ClientNamespace) :
    def on_verify_token_result(self, data):
        print(data)

    def on_verify_otp_result(self, data):
        print(data)

    def on_add_details_result(self, data): 
        print(data)