import argparse
import socket

from dask import delayed, compute
from dask.diagnostics import ProgressBar

def port_open(ip:str, port:int) -> bool:
    try:
        s = get_socket(ip, port)
        s.connect((ip,port))
        s.shutdown(2)
        return (True, port)
    except Exception as e:
        s.close()
    return (False, port)

def get_socket(ip:str, port:int) ->socket.socket:
    if ":" in ip:
        return socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def main(args):


    port_lower = int(args.port_start)
    port_upper = int(args.port_end) + 1

    to_scan = []

    print(f"Scanning {args.ip} from port {port_lower} to {port_upper}")

    for i in range(port_lower,port_upper):
        to_scan.append(delayed(port_open)(args.ip, i))

    with ProgressBar():
        res = compute(*to_scan)

    print(f"Closed Ports: {' '.join([str(p[1]) for p in res if not p[0]])}")
    
    print(f"Open Ports: {' '.join([str(p[1]) for p in res if p[0]])}")
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", "--ip", help="Target IP Address")
    parser.add_argument("-start", "--port-start", help="Lower end of ports to scan.")
    parser.add_argument("-end", "--port-end", help="Upper end of ports to scan.")

    args = parser.parse_args()
    
    main(args)
    