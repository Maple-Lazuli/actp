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
class IPv6Header:
    version_class_flow: bytes = b"\x60\x00\x00\x00"
    payload_len: bytes = b"\x00\x00"
    hop_limit: bytes = b"\xff"
    src_address: bytes = b"\x00"*16
    dst_address: bytes = b"\x00"*16

    next_header: bytes = b"\x06" # \x3a ICMP  \x06 TCP

    def set_payload_len(self, size):
        self.payload_len = struct.pack(">H",size)
    def set_next_header(self, next_header:bytes):
        self.next_header = next_header
    def set_hop_limit(self, hop_limit: int):
        self.hop_limit = struct.pack(">B", hop_limit)
    def get_header(self):
        return self.version_class_flow + self.payload_len + self.next_header + self.hop_limit + self.src_address + self.dst_address


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
    protocol: bytes = b'\x06' #6 for TCP 1 for ICMP 21 for UDP
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


