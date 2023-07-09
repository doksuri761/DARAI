import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8009)
sock.connect(server_address)
request = "POST /enqueue/{}?item={}&key={} HTTP/1.1\r\nHost: {}.com\r\n\r\n"
sock.sendall(request.encode())
response = sock.recv(4096)
response_text = response.decode()
sock.close()
print(response_text)
