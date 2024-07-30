import socket
import time

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
    s.connect(("pyctf.class.net", 8086))
    lines = []
    chunk = s.recv(2048)
    try: 
        while True:
            lines.append(chunk)
            chunk = chunk.decode()
            
            if chunk.find("GAME OVER") != -1:
                break

            for l in chunk.split("\n"):
                print(l)
            command = input("Command: ")
            
            s.send(f'{command}\n'.encode())
            time.sleep(0.1)
            chunk = s.recv(2048)
    except:
        pass

    for line in lines[-3:-1]:
        for l in line.decode().split("\n"):
            print(l)

    
