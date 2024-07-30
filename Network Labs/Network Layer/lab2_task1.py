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
    def get_header(self):
        return self.type + self.code + self.reserved + self.checksum + self.target + self.options

class ICMPOptions:
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
        return self.type + self.src_length + self.src_address  #+  self.dst_length + self.dst_address
    
if __name__ == "__main__":
    ipv6_etherheader = EthernetHeader("33:33:00:00:00:01", "00:50:56:01:4e:df", b"\x86\xdd")

    src_address = ipv6_to_bytes("a:c:7:9:d419:bd42:16fb:a917")

    dst_address = ipv6_to_bytes("a:c:7:9:5107:2e3:22a9:3cfd")

    icmp_options = ICMPOptions()
    icmp_options.set_type(b"\x01")
    icmp_options.set_src_length(1)
    icmp_options.set_src_address(addr_to_bytes("00:50:56:01:4e:df"))
    icmp_options.set_dst_length(1)
    icmp_options.set_dst_address(b"\x00" * 6)

    icmpv6_header = ICMPv6()
    icmpv6_header.set_type(b"\x87")
    icmpv6_header.set_code(b"\x00")
    icmpv6_header.set_checksum(b"\x00\x00")
    icmpv6_header.set_target_ip(dst_address)
    icmpv6_header.set_options(icmp_options.get_header())

    ipv6 = IPv6Header()
    ipv6.set_payload_len(len(icmpv6_header.get_header()))
    ipv6.set_next_header(b"\x3a")
    ipv6.set_hop_limit(20)
    ipv6.set_src_ip(src_address)
    ipv6.set_dst_ip(dst_address)

    packet = ipv6_etherheader.get_header() + ipv6.get_header() + icmpv6_header.get_header()

    device = "vmxnet3 Ethernet Adapter"
    cno.rawsend_cksum_ipv6(packet, device)

    print(" ".join([hex(int(b))[2:].zfill(2) for b in packet]))