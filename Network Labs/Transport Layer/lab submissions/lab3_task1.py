import argparse
from dataclasses import dataclass, field
import struct
import cno_net_helper as cno

dev = "vmxnet3 Ethernet Adapter"

def port_to_bytes(port):
    return struct.pack(">H", port)

def num_to_32bit(num):
    return struct.pack(">L", num)


def ipv6_to_bytes(adder):
    parts = adder.split(":")
    return struct.pack(">8H", *[int(p,16) for p in parts])

def addr_to_bytes(addr, base = 16, sep=":"):
    addr = addr.lower()
    parts = addr.split(sep)
    return struct.pack(f">{len(parts)}B", *(int(p,base) for p in parts))

def packet_dump(packet):
    return " ".join(hex(int(b))[2:].zfill(2) for b in packet )

@dataclass
class EthernetHeader:
    dst_mac: bytes = b'\x00'*6
    src_mac: bytes = b'\x00'*6
    type_code: bytes = b'\x00'*2
    
    def get_header(self):
        return self.dst_mac + self.src_mac + self.type_code

@dataclass
class IPHeader:
    version_ihl: bytes = b'\x45'
    service_type: bytes = b'\x00'
    total_length: bytes = b'\x00' * 2 # length measureed in octets
    id: bytes = b'\x00' *2
    flags_frag_offset: bytes = b"\x00" * 2
    ttl: bytes = b'\x0f'
    protocol: bytes = b'\x00' #6 for TCP 1 for ICMP 21 for UDP
    checksum: bytes = b'\x00' * 2
    src_address: bytes = b'\x00' * 4
    dst_address: bytes = b'\x00' * 4
    options: bytes = None
    
    def update_length(self, next_header = None):
        octets = len(self.get_header())

        octets += len(next_header) if next_header is not None else 0

        self.total_length = struct.pack(">H", octets)

    def add_option(self, option):
        self.options += option

    def get_header(self):
        header = self.version_ihl + self.service_type + self.total_length + self.id + self.flags_frag_offset + self.ttl + self.protocol + self.checksum + self.src_address + self.dst_address
        if self.options is not None:
            header += self.options
        return header

@dataclass
class TCPHeader:
    src_port: bytes = b"\x00" * 2
    dst_port: bytes = b"\x00" * 2
    seq_num: bytes = b"\x00" * 4
    ack_num: bytes = b"\x00" * 4
    data_offset_flags: bytearray = field(default_factory=bytearray)
    window: bytes = b"\x00\xff"
    checksum: bytes = b"\x00" * 2
    urgent_ptr: bytes = b"\x00" *2
    options: bytes = None
    data: bytes = None

    def __post_init__(self):
        self.data_offset_flags = bytearray([80,0])

    def toggle_flag(self, flags: list):
        if 'FIN' in flags:
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 0)
        if 'SYN' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 1)
        if 'RST' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 2)
        if 'PSH' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 3)
        if 'ACK' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 4)
        if 'URG' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 5)
        if 'ECE' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 6)
        if 'CWR' in flags:                                          
            self.data_offset_flags[1] = self.data_offset_flags[1] ^ (2 ** 7)

    def set_data_offset(self, new_value:bytes):
        self.data_offset_flags = new_value + self.data_offset_flags[1]
        
            
    def get_header(self):
        header = self.src_port + self.dst_port + self.seq_num + self.ack_num + bytes(self.data_offset_flags) + self.window + self.checksum + self.urgent_ptr
        if self.options is not None:
            header += self.options   
        if self.data is not None:
            header += self.data
        return header


def main(args):
    server_ip = addr_to_bytes(args.source_ip,10,".")
    server_mac = addr_to_bytes(args.source_mac)
    client_ip = addr_to_bytes(args.dest_ip,10,".")
    client_mac = addr_to_bytes(args.dest_mac)
    server_port = port_to_bytes(int(args.sport))
    client_port = port_to_bytes(int(args.dport))

    eth_header = EthernetHeader(client_mac, server_mac, b"\x08\x00")
    ip4_header = IPHeader(protocol = b"\x06", src_address = server_ip, dst_address = client_ip)
    
    ack = num_to_32bit(0)
    seq = num_to_32bit(int(args.sequence_number))

    tcp_header = TCPHeader(src_port=server_port, dst_port=client_port, seq_num = seq, ack_num = ack, window=port_to_bytes(8212))
    tcp_header.toggle_flag(["RST"])

    ip4_header.update_length(tcp_header.get_header())

    packet = eth_header.get_header() + ip4_header.get_header() + tcp_header.get_header()

    cno.rawsend_cksum_ipv4(packet, dev = arg.interface )

    print(packet_dump(packet=packet))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-smac", "--source-mac", help="Source Mac Address")
    parser.add_argument("-dmac", "--dest-mac", help="Destination Mac Address")
    parser.add_argument("-sip", "--source-ip", help="Source IP Address")
    parser.add_argument("-dip", "--dest-ip", help="Destination IP Address")
    parser.add_argument("-sport", "--source-port", help="Source Port")
    parser.add_argument("-dport", "--dest-port", help="Destination Port")
    parser.add_argument("-seq", "--sequence-number", help="Sequence Number")
    parser.add_argument("-if", "--interface", help="Interface To Use")
    main(parser)
