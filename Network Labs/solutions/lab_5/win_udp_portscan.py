# UDP port scanner
# Windows 10 builds of Python 3 only-- depends on behavior of Winsock API

import socket
import sys

ip = sys.argv[1]
portstart = int(sys.argv[2])
portend = int(sys.argv[3])

for port in range(portstart, portend):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)
        sock.sendto(b'\x00', (ip, port))
        data, host = sock.recvfrom(1024)
    # on Windows, an ICMP "Destination Unreachable" message causes the next recvfrom()
    # call to raise a ConnectionResetError (WSAECONNRESET) -- see Winsock docs
    except ConnectionResetError:
        print('{}\tCLOSED'.format(port))
        continue
    except socket.timeout:
        print('{}\tOPEN OR DROPPED'.format(port))
        continue
    print('{}\tOPEN; RESPONDED ({})'.format(port, data))
