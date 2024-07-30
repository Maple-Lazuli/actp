import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("192.168.0.62", 8888)) # if you want to use send
s.sendto(b"Hello, UDP",("172.16.91.3", 8888))
#to recvfrom, would need to bind to a port
s.close()
