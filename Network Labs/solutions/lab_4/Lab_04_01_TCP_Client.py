import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("172.16.91.3", 8888))
s.send(b"Hello, my name is packet\n")
s.close()
