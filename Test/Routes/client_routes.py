from socketio import ClientNamespace

class client_routes(ClientNamespace) :
    def on_verify_token_result(self, data):
        print(data)