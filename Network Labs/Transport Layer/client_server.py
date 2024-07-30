import socket

def create_udp_server(port:int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("0.0.0.0", port))
        while True:
            data = s.recvfrom(1024)
            if not data[0]:
                break
            message, source = data
            print(f"{source[0]} at {source[1]} says: {message.decode()}")


def create_udp_client(server:str, port:int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:        
        data_to_send = "Getting Started"
        while len(data_to_send.strip()) != 0:
            data_to_send = input(f"Data to send to {server} at {port}:")
            s.sendto(data_to_send.encode(), (server, port))


def create_tcp_server(port:int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen()
        connection, address = s.accept()
        with connection:
            print(f"{address[0]} connected on {address[1]}.")
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print(data.decode())


def create_tcp_client(server:str, port:int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, port))
        
        data_to_send = "Getting Started"
        while len(data_to_send.strip()) != 0:
            data_to_send = input(f"Data to send to {server} at {port}:")
            s.send(data_to_send.encode())
    