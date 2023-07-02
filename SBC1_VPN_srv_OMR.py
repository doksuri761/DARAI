from python_wireguard import Key, ClientConnection, Server
private, public = Key.key_pair()
print(public)
server = Server("wg-srv", private, "10.0.0.1/24", 12345)
server.enable()
