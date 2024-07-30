import argparse
import struct

import cno_net_helper as cno

def addr_to_bytes(addr, base = 16, sep=":"):
    addr = addr.lower()
    parts = addr.split(sep)
    return struct.pack(f">{len(parts)}B", *(int(p,base) for p in parts))

def create_eth_header_for_arp(src_mac: str) -> bytes:
    dst = b"\xff" * 6
    src = addr_to_bytes(src_mac)
    typ = b"\x08\x06"
    return dst + src+ typ

def create_arp_request_payload(src_mac: str, src_ip: str, dst_ip: str) -> bytes:
    arpreq= b"\x00\x01" # HwType
    arpreq+= b"\x08\x00" # Proto Type
    arpreq+= b"\x06" # HwAddrLen
    arpreq+= b"\x04" # Proto AddrLen
    arpreq+= b"\x00\x01" # Op Code (Req)
    arpreq+= addr_to_bytes(src_mac) # my mac
    arpreq+= addr_to_bytes(src_ip, base = 10, sep=".") # YOUR IP (SRC)
    arpreq+= b"\x00" * 6 # Zeroed on Request
    arpreq+= addr_to_bytes(dst_ip, base = 10, sep=".") # THEIR IP(DST)

    return arpreq

def main(smac, sip, dip, device):

    packet = create_eth_header_for_arp(smac) + create_arp_request_payload(smac, sip, dip)

    cno.rawsend(packet, dev=device)



if __name__== "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-smac", "--source-mac", help="Source Mac Address")
    parser.add_argument("-sip", "--source-ip", help="Source IP Address")
    parser.add_argument("-dip", "--dest-ip", help="Destination IP Address")
    parser.add_argument("-if", "--interface", help="Interface To Use")
    
    args = parser.parse_args()

    main(args.source_mac, args.source_ip, args.dest_ip, args.interface)

    #sample command:
    # python .\lab1_task3.py -smac "00:50:56:01:4e:df" -sip 172.16.91.10 -dip 172.16.91.190 -if "vmxnet3 Ethernet Adapter"