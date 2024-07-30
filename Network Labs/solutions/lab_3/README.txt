NOTE: cno_net_helper.py should be located in the lab_3 directory to correctly resolve to the import statement listed in this lab.

Terminology:
	Victim: Host that is sending the Neighbor advertisement, Neighbor solicitation, or router advertisement:
	Server: Specific target if there is one (not relevant for router advertisement

Flow of Lab:
	Waits for a TCP packet from Victim to Server with the PSH and ACK flags set, then sends a RST packet to Victim "from" the Server (Just impersonating the server, doesn't actually need to come from the Server machine for example if you leveraged this with a mitm).

How to run:
	Setup a listening netcat connecton (any port), connect another netcat connection to the listening port, run 'python3 ./Lab_03_01_TCP_Reset -i "<interface_to_send_on>" <victim_ip> <server_ip> <server_port>'. This will start listening on the wire for the packet outlined above in "Flow of Lab".
	Next, send data from the "client" netcat connection. You should see a connection reset by peer on the client side.
	
	
