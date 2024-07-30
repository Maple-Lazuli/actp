import argparse
import socket
import functions as f
import cno_net_helper as cno

def sent_packet(args, source_port, dest_port):
    if ":" in args.target_ip: 
        target_ip = socket.inet_pton(socket.AF_INET6,args.target_ip)
        packet_type = b"\x08\xdd"
    else:
        target_ip = socket.inet_pton(socket.AF_INET,args.target_ip)
        packet_type = b"\x08\x00"

    if ":" in args.source_ip: 
        source_ip = socket.inet_pton(socket.AF_INET6,args.source_ip)
    else:
        source_ip = socket.inet_pton(socket.AF_INET,args.source_ip)

    target_mac = f.addr_to_bytes(args.target_mac)
    source_mac = f.addr_to_bytes(args.source_mac)


    eth = f.EthernetHeader(target_mac, source_mac, packet_type)

    tcp = f.TCPHeader(src_port=f.port_to_bytes(source_port), dst_port=f.port_to_bytes(dest_port))

    tcp.toggle_flag(['SYN'])

    if packet_type == b"\x08\xdd":
        ip = f.IPv6Header(src_address=source_ip, dst_address=target_ip)
        ip.set_payload_len(len(tcp.get_header()))
        packet = eth.get_header() + ip.get_header() + tcp.get_header()
        cno.rawsend_cksum_ipv4(packet, dev = f.dev )  
    else:
        ip = f.IPHeader(src_address=source_ip, dst_address=target_ip)
        ip.update_length(tcp.get_header())
        packet = eth.get_header() + ip.get_header() + tcp.get_header()
        cno.rawsend_cksum_ipv4(packet, dev = f.dev )  
    


def main(args):
    dest = 9000
    for i in range(int(args.port_start), int(args.port_end) + 1):
        sent_packet(args, i, dest)

if __name__ == "__main__":

