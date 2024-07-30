import pickle
import socket 
import struct

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 5555))

    data = sock.recv(2028)
    data = pickle.loads(data)

    endianess = chr(data[0])
    data = data[1:]
    l1, l2 = struct.unpack(f"{endianess}LL", data)

    response = pickle.dumps(struct.pack(f"{endianess}L", l1 + l2))
    sock.sendall(response)
    
    message = sock.recv(2028)
    print(message.decode())