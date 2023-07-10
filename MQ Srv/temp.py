import socket
import timeit
import threading
import random


def send(a):
    file = open(f"test{a}.csv", "w")
    file.write("Conn Time., Send Time, Recv Time\n")
    t = timeit.default_timer()
    for _ in range(1000):
        t1 = timeit.default_timer()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 8009)
        sock.connect(server_address)
        t2 = timeit.default_timer()
        request = f"POST /enqueue/OMR?item={None}&key={None} HTTP/1.1\r\nHost: {None}.com\r\n\r\n"
        sock.sendall(request.encode())
        t3 = timeit.default_timer()
        response = sock.recv(4096)
        response_text = response.decode()
        t4 = timeit.default_timer()
        sock.close()
        file.write(f"{round((t2 - t1) * 1000, 5)}, {round((t3 - t2) * 1000, 5)}, {round((t4 - t3) * 1000, 5)}\n")
    print(timeit.default_timer() - t, " for 1000 times")
    file.close()


ths = [threading.Thread(target=send, args=[i]) for i in range(10)]
for th in ths:
    th.start()
    th.join()
