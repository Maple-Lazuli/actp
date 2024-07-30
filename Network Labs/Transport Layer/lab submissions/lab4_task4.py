#!/usr/bin/python3.7
import socket
import struct
import time
###########################################################
#
#   Lab 4 Task 2 - Multicast Server
#
#       Server that can receive UDP datagrams on
#       Multicast address
#
###########################################################

'''
For help getting subscribed to the multicast group look here:
search rfc for socket options......
rfc3493.txt

'''

def reciever(dst_ip, dst_port):

    # TODO: Configure address info for connection
    addrinfo = socket.getaddrinfo(dst_ip, None)[0]
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])

    # Create and configure UDP socket (DGRAM)
    my_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # Bind it to the port
    my_sock.bind(('', dst_port))

    # TODO: Configure socket for multicast
    mreq = group_bin + struct.pack('@I', 0)
    my_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, printing any data we receive
    while True:
        data, sender = my_sock.recvfrom(1500)
        print(str(sender) + '  ' + repr(data.decode()))


def sender(dst_ip, dst_port):
    my_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    for i in range(1, 99999999):
        data = (b"Sending packet #%d\n" % (i))
        my_sock.sendto(data, (dst_ip, dst_port))
        time.sleep(5)

    my_sock.close()

if __name__ == "__main__":
    address = "ff02::c:c:c:1"
    port = 6660

    # For sending
    # sender(address, port)

    # For recieving
    # reciever(address, port)