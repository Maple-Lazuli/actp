import pickle
import random
import socket
import struct
import sys
import threading
from datetime import datetime

server_port = 5555

def handle_connection(sock, remote_addr):
    try:
        # generate the random variables        
        endianness = random.choice('<>').encode()
        num1 = random.randint(0, 0xFFFF)
        num2 = random.randint(0, 0xFFFF)

        # pack the values, pickle them, and send
        pack_str = endianness + b'cLL'
        packed_nums = struct.pack(pack_str, endianness, num1, num2)
        sock.sendall(pickle.dumps(packed_nums))

        # compare the expected value against what we expect from the user
        expect_data = pickle.dumps(struct.pack(endianness + b'L', num1 + num2))
        client_data = sock.recv(len(expect_data))

        # if they packed the sum and pickled it correctly, print out that they did it correctly
        if client_data == expect_data:
            sock.sendall(b'The empire did nothing wrong, dirty rebel.')
            print(f'{datetime.now()} - {str(remote_addr)} got the SECRET KEY!')
        else:
            sock.sendall(b'INCORRECT! Terminating connection!')
            print(f'{datetime.now()} - {str(remote_addr)} gave incorrect value {client_data}')

    except:
        print(sys.exc_info())
        print(f'{datetime.now()} - EXCEPTION! {str(remote_addr)} was denied!')

    finally:
        print()
        sock.close()


# IPv4, TCP by default
sock = socket.socket()
sock.bind(('', server_port))
sock.listen(15)

try:
    while True:
        new_sock, remote_addr = sock.accept()
        print(f'{datetime.now()} - Got a new connection from {str(remote_addr)}')
        threading.Thread(target=handle_connection, args=(new_sock, remote_addr)).start()
finally:
    sock.close()
