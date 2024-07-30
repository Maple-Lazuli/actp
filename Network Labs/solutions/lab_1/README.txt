NOTE: cno_net_helper.py should be located in the lab_1 directory to correctly resolve to the import statements listed in these labs.

Terminology:
	Host A - Host that is sending the unsolicited arp reply
	Victim - Host that the unsolicited arp reply is being sent to
	Server - The server that Host A is trying to block Victim's access to

Flow of Lab:
	Lab_01-03_ARP_request: Host A sends an ARP request to the broadcast address asking for the MAC address of a given IP address. On reply, the (MAC, IP) maping is put into Host A's arp cache
	Lab_01-04_ARP_cache_poisoning: Host A sends an unsolicted ARP reply to Victim telling it the wrong MAC address for Server. Victim gladly puts this false mapping in its ARP cache and breaks the connection to Server.
	Lab_01-mitm: Host A sends an unsolicited ARP pely to both Victim and Server. They both then will send their communications between each other through Host A rather than directly between Server and Victim.
	

What to change in Solution:
	Lab_01-03_ARP_request: dev, dst_ip, src_ip, src_mac
	Lab_01-04_ARP_cache_poisoning: dev, src_mac, src_ip, dst_ip, dst_mac, spoof_ip, spoof_mac
	Lab_01-mitm: dev, src_ip, target_a_ip, target_b_ip, src_mac, target_a_mac, target_b_mac

How to Run:
	Lab_01-03_ARP_request: python3 ./Lab_01-03_ARP_request.py
	Lab_01-04_ARP_cache_poisoning: python3 ./Lab_01-04_ARP_cache_poisoning.py
	Lab_01-mitm: python3 ./Lab_01-mitm.py

NOTE: some students will elect to use SCAPY to complete their labs. Suggestion to the instructor is to either have them manually do this first lab so you can validate/track their understanding or get a little familiar with how SCAPY works - it's super easy!!!

NOTE: firewalls normally screw up connections - especially in Windows CNO.  Disable the firewall/flush the tables if your having ping/connectivity issues.  Boxes get re-imaged between each quarters. 
