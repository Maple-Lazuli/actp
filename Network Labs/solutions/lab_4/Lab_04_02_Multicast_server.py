#!/user/bin/python3.7
import socket
import struct

###########################################################
#
#   Lab 4 Task 2 - Multicast Server
#
#       Server that can receive UDP datagrams on
#       Multicast address
#
###########################################################

"""
Phase 1:
man ipv6
/usr/include/linux/in6.h
pydoc3 socket (look in the DATA section near the end)
man setsockopt (what are the arguments to setsockopt?)

Phase 2:
search rfc for ipv6_mreq
rfc3493.txt
IPV6_JOIN_GROUP (It used to be IPV6_ADD_MEMBERSHIP but that was obsoleted by later RFC’s). 
It's defined in /usr/linux/x86_64-linux-gnu/bits/in.h
"""


# Configure address info for connection
dst_ip = "FF02::777:777:777"
dst_port = 7777

# Create and configure UDP socket (DGRAM)
my_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

# OPTIONAL: Allow multiple copies of this program on one machine
my_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind it to the port
my_sock.bind(('', dst_port))

group_bin = socket.inet_pton(socket.AF_INET6, dst_ip)
group = group_bin + struct.pack('@I',0) 
my_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, group) #41

# Loop, printing any data we receive
while True:
    data, sender = my_sock.recvfrom(1500)
    print(str(sender) + '  ' + repr(data.decode()))
