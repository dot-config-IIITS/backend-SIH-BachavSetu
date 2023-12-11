from socketio import ClientNamespace

class admin_routes(ClientNamespace) :
    def on_verify_token_result(self, data):
        print(data)