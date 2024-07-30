#!/usr/bin/python3.7
import struct
import cno_net_helper as cno  # cno_net_helper.py should be the same folder


# FOR LINUX - comment out the Windows line below
#dev = "ens33"  # Device to send packet out
# FOR WINDOWS - comment out the Linux line above
dev = "vmxnet3 Ethernet Adapter"  # Device to send packet out

# Multicast address
ipv6_multicast_mac = cno.mac_str_to_bin("33:33:00:00:00:01")  # IPv6 Multicast MAC

# Destination
dst_mac = ipv6_multicast_mac
dst_ipv6 = cno.ipv6_str_to_bin("a:c:7:9:1857:e75a:6d1e:a8b2")
#dst_ipv6_mcast = cno.ipv6_str_to_bin("ff02::1:ff00:1")
#example solicited node addr "ff02::1:ff41:b223"


# Source
src_mac = cno.mac_str_to_bin("00:50:56:01:44:c2")   		# Host MAC
src_ipv6 = cno.ipv6_str_to_bin("a:c:7:9:c1e9:e063:fd82:fdb7")	# Host IPv6 address


# ICMPv6 and ICMPv6 Options
icmpv6_hdr = b"\x87"    	# Type: 135 (neighbor solicitation)
icmpv6_hdr += b"\x00"  		# Code: 0
icmpv6_hdr += b"\x00" * 2 	# Checksum: calculated in cno.rawsend_cksum_ipv6()
icmpv6_hdr += b"\x00" * 4  	# Reserved: 0
icmpv6_hdr += dst_ipv6    	# Target IPv6 for solicitation

# ICMPv6 header options
icmpv6_option = b"\x01"  	# Type: Source Link-Layer address (1)
icmpv6_option += b"\x01"  	# Len: 8 
icmpv6_option += src_mac  	# Source MAC

# Calculate ICMPv6 length
icmpv6_hdr += icmpv6_option
icmpv6_hdr_len = struct.pack('>H', len(icmpv6_hdr))

# IPv6
ipv6_hdr = b"\x60\x00\x00\x00"  # Version (4 bit): 6 (0x6)
				# Traffic class (8 bit): 0 (0x00)
				# Flow label (20 bit): 0  (0x00000)

# Payload len (2 bytes): ICMPv6 header + ICMPv6 options
ipv6_hdr += icmpv6_hdr_len
ipv6_hdr += b"\x3a"            				# Next header: 58 (ICMPv6)
ipv6_hdr += b"\xff"            				# Hop limit: 255 (default)
ipv6_hdr += src_ipv6           				# Source IPv6 adresses
ipv6_hdr += dst_ipv6           				# Destination IPv6

# Ethernet
eth_hdr = ipv6_multicast_mac  				# Destination MAC
eth_hdr += src_mac            				# Source MAC
eth_hdr += struct.pack(">H", cno.ETH_TYPES['IPv6'])	# Type: IPv6

# Contruct Ethernet frame
eth_frame = eth_hdr + ipv6_hdr + icmpv6_hdr

# Send the packet with checksum
cno.rawsend_cksum_ipv6(eth_frame, dev)
#cno.rawsend(eth_frame, dev) # use instead if the checksum is creating issues
