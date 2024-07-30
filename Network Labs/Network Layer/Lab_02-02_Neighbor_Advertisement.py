#!/usr/bin/python3.7
import socket
import struct
import cno_net_helper as cno  # cno_net_helper.py should be the same folder


# FOR LINUX - comment out the Windows line below
#dev = "ens33"  # Device to send packet out
# FOR WINDOWS - comment out the Linux line above
dev = "vmxnet3 Ethernet Adapter"  # Device to send packet out

# Multicast address
ipv6_multicast_mac = cno.mac_str_to_bin("33:33:00:00:00:01")

# Destination
dst_mac = ipv6_multicast_mac
dst_ipv6 = cno.ipv6_str_to_bin("a:c:7:9::18")
#dst_ipv6_mcast = cno.ipv6_str_to_bin("ff02::1:ff00:18")

# Source
src_mac = cno.mac_str_to_bin("00:50:56:01:44:c2")   		# Host MAC
src_ipv6 = cno.ipv6_str_to_bin("a:c:7:9:c1e9:e063:fd82:fdb7")	# Host IPv6 address


def make_icmpv6_hdr(dst_ipv6, src_mac):
    # ICMPv6 and ICMPv6 Options
    icmpv6_hdr = b"\x88"		# Type: 136 (neighbor advertisement)
    icmpv6_hdr += b"\x00"		# Code: 0

    # Checksum : Set to 0.  Calculated in send rawsend_cksum
    icmpv6_hdr += b"\x00" * 2
    icmpv6_hdr += b"\x60" + (b"\x00"*3)	# Flags: None set
    icmpv6_hdr += dst_ipv6              # Target IPv6 for advertisement

    # ICMPv6 header options
    icmpv6_option = b"\x02"  		# Type: Target Link-Layer address (2)
    icmpv6_option += b"\x01"  		# Len: 1 * 8 bytes
    icmpv6_option += src_mac  		# Source MAC

    # Calculate ICMPv6 length
    icmpv6_hdr += icmpv6_option
    return icmpv6_hdr


icmpv6_hdr = make_icmpv6_hdr(dst_ipv6, src_mac)
ipv6_hdr = b"\x60\x00\x00\x00"  # Version (4 bit): 6 (0x6)
				# Traffic class (8 bit): 0 (0x00)
				# Flow label (20 bit): 0  (0x00000)

# Payload len (2 bytes): ICMPv6 header + ICMPv6 options
ipv6_hdr += struct.pack(">H", len(icmpv6_hdr))
ipv6_hdr += b"\x3a"             # Next header: 58 (ICMPv6)
ipv6_hdr += b"\xff"             # Max hop limit: 255
ipv6_hdr += src_ipv6            # Source IPv6 adresses
ipv6_hdr += dst_ipv6            # Destination ICMPv6

#####################################################################
# Ethernet
#####################################################################
eth_hdr = ipv6_multicast_mac  				# Destination MAC
eth_hdr += src_mac             				# Source MAC
eth_hdr += struct.pack(">H", cno.ETH_TYPES['IPv6'])	# Type: IPv6

# Contruct Ethernet frame
eth_frame = eth_hdr + ipv6_hdr + icmpv6_hdr

# Send the packet with checksum
cno.rawsend_cksum_ipv6(eth_frame, dev)
#cno.rawsend_ipv6(eth_frame, dev) # use instead if the checksum is creating issues
