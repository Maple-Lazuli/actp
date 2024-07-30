import struct
import cno_net_helper as cno

def ipv6_to_bytes(adder):
    parts = adder.split(":")
    return struct.pack(">8H", *[int(p,16) for p in parts])

def addr_to_bytes(addr, base = 16, sep=":"):
    addr = addr.lower()
    parts = addr.split(sep)
    return struct.pack(f">{len(parts)}B", *(int(p,base) for p in parts))

class EthernetHeader:
    def __init__(self, dst_mac: str, src_mac: str, type_code: bytes):
        self.dst_mac = addr_to_bytes(dst_mac)
        self.src_mac = addr_to_bytes(src_mac)
        self.type_code = type_code

    def get_header(self):
        return self.dst_mac + self.src_mac + self.type_code
    
class IPv6Header:
    def __init__(self):
        self.version_class_flow = b"\x60\x00\x00\x00"
    def set_payload_len(self, size):
        self.payload_len = struct.pack(">H",size)
    def set_next_header(self, next_header:bytes):
        self.next_header = next_header
    def set_hop_limit(self, hop_limit: int):
        self.hop_limit = struct.pack(">B", hop_limit)
    def set_src_ip(self, address: bytes):
        self.src_address = address
    def set_dst_ip(self, address:bytes):
        self.dst_address = address
    def get_header(self):
        return self.version_class_flow + self.payload_len + self.next_header + self.hop_limit + self.src_address + self.dst_address
    
# DIY Neighbor Solicit
class ICMPv6:
    def __init__(self):
        self.reserved = b"\x00" * 4
    def set_type(self,type_code):
        self.type = type_code
    def set_code(self,code):
        self.code = code
    def set_checksum(self, checksum):
        self.checksum = checksum
    def set_target_ip(self, address):
        self.target = address
    def set_options(self, options):
        self.options = options
    def set_reserved(self, reserved):
        self.reserved = reserved
    def get_header(self):
        return self.type + self.code + self.reserved + self.checksum + self.target + self.options

class ICMPOptions: # Source link layer address
    def set_type(self, type_code):
        self.type = type_code
    def set_src_length(self, length):
        self.src_length = struct.pack(">B", length)
    def set_src_address(self, address):
        self.src_address = address
    def set_dst_length(self, length):
        self.dst_length = struct.pack(">B", length)
    def set_dst_address(self, address):
        self.dst_address = address
    def get_header(self):
        return self.type + self.src_length + self.src_address
    
class ICMPv6_Router_Advertisement:
    def __init__(self):
        self.reserved = b"\x00" * 4
        
    def set_type(self,type_code):
        self.type = type_code
        
    def set_code(self,code):
        self.code = code
        
    def set_checksum(self, checksum):
        self.checksum = checksum
        
    def set_current_hop_limit(self, limit):
        self.hop_lim = struct.pack(">B", limit)
        
    def set_reserved(self, reserved_bits):
        self.reserved = reserved_bits
        
    def set_lifetime(self, lifetime): #seconds
        self.lifetime = struct.pack(">H", lifetime)
        
    def set_reach_time(self, reach_time): # milliseconds
        self.reach_time = struct.pack(">L", reach_time)
        
    def set_retrans_time(self, trans_time): #milliseconds
        self.retrans_time = struct.pack(">L", trans_time)
        
    def set_options(self, options):
        self.options = options
        
    def get_header(self):
        return self.type+ self.code + self.checksum + self.hop_lim + self.reserved + self.lifetime + self.reach_time + self.retrans_time + self.options

class ICMPOptionsPrefixInformation:
    def set_type(self, type_code):
        self.type = type_code
    def set_length(self, length):
        self.length = length
    def set_prefix_length(self, length):
        self.prefix_length = struct.pack(">B", length)
    def set_reserved(self, reserved):
        self.reserved = reserved
    def set_valid_lifetime(self, lifetime):
        self.valid_lifetime = struct.pack(">L", lifetime)
    def set_preferred_lifetime(self, lifetime):
        self.preferred_lifetime = struct.pack(">L", lifetime)
    def set_reserved2(self, reserved):
        self.reserved2 = reserved
    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_header(self):
        return self.type + self.length + self.prefix_length + self.reserved + self.valid_lifetime + self.preferred_lifetime + self.reserved2 + self.prefix

if __name__ == "__main__":
    ipv6_etherheader = EthernetHeader("33:33:00:00:00:01", "00:50:56:01:4e:df", b"\x86\xdd")
    src_address = ipv6_to_bytes("fe80:0:0:0:d419:bd42:16fb:a917") 
    new_prefix = ipv6_to_bytes("9:9:9:0c:0:0:0:0")
    dst_address = ipv6_to_bytes("ff02:0:0:0:0:0:0:1") 

    icmp_prefix_option = ICMPOptionsPrefixInformation()
    icmp_prefix_option.set_type(b"\x03")
    icmp_prefix_option.set_length(b"\x04")
    icmp_prefix_option.set_prefix_length(64)
    icmp_prefix_option.set_reserved(b"\xc0")
    icmp_prefix_option.set_valid_lifetime(120)
    icmp_prefix_option.set_preferred_lifetime(120)
    icmp_prefix_option.set_reserved2(b"\x00"*4)
    icmp_prefix_option.set_prefix(new_prefix)


    icmp_options = ICMPOptions()
    icmp_options.set_type(b"\x01")
    icmp_options.set_src_length(1)
    icmp_options.set_src_address(addr_to_bytes("00:50:56:01:4e:df"))

    icmpv6_header = ICMPv6_Router_Advertisement()
    icmpv6_header.set_type(b"\x86")
    icmpv6_header.set_code(b"\x00")
    icmpv6_header.set_checksum(b"\x00\x00")
    icmpv6_header.set_current_hop_limit(64)
    icmpv6_header.set_reserved(b"\x00") 
    icmpv6_header.set_lifetime(120)
    icmpv6_header.set_reach_time(1000)
    icmpv6_header.set_retrans_time(0)
    icmpv6_header.set_options(icmp_prefix_option.get_header() + icmp_options.get_header())

    ipv6 = IPv6Header()
    ipv6.set_payload_len(len(icmpv6_header.get_header()))
    ipv6.set_next_header(b"\x3a")
    ipv6.set_hop_limit(255)
    ipv6.set_src_ip(src_address)
    ipv6.set_dst_ip(dst_address)
    dev = "vmxnet3 Ethernet Adapter"
    router_advertisement = ipv6_etherheader.get_header() + ipv6.get_header()  +  icmpv6_header.get_header()
    cno.rawsend_cksum_ipv6(router_advertisement, dev)
    # Sorry its messy, felt pressed for time. Will clean up and resubmit as time allows.
    # Hexdump of packet created by this code for revew in hex packet decoder:
    # 33 33 00 00 00 01 00 50 56 01 4e df 86 dd 60 00 00 00 00 38 3a 14 fe 80 00 00 00 00 00 00 d4 19 bd 42 16 fb a9 17 fe 80 00 00 00 00 00 00 95 b0 73 50 42 ee 60 fb 86 00 00 00 14 00 00 0a 00 00 03 e8 00 00 03 e8 01 01 00 50 56 01 4e df 03 04 10 20 00 00 00 14 00 00 00 14 00 00 00 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00
