NOTE: cno_net_helper.py should be located in the lab_5 directory to correctly resolve to the import statements listed in these labs.

Terminology:
	Victim: Host you are port scanning

Flow of Lab:
	Lab_05_01_Port_Scanner: Does a full tcp port scan on Victim
	Lab_05_02_*: Does a stealth tcp port scan on victim using a raw sender to do the port scan and a raw sniffer to listen for results coming back

How to run Lab_05_02_*:
	- Open config.txt and change ip and mac under 'target' to the mac and ip of Victim. This will need to be 
your actual ip address and not localhost
	- Then change ip and mac to your machine's ip and mac to send the port scan from. You don't need to change the port arguments if you're scanning all 65536 ports.
	Lab_05_01_Port_scanner:  python3 ./Lab_05_01_Port_scanner -i <victim_ip>
	Lab_05_02_*:
		Lab_05_02_Tcp_Raw_Sniffer: python3 ./Lab_05_02_Tcp_Raw_Sniffer -i <interface> target
			*target at the end should the literal word "target" to tell the code what config to use from config.txt
		Lab_05_02_Tcp_Raw_Sender: python3 ./Lab_05_02_Tcp_Raw_Sender -i <interface> target
			*target at the end should the literal word "target" to tell the code what config to use from config.txt
		*Run The sniffer first then run the sender as outlined above and you should slowly see open ports being printed out (You can run a python server on the target as a sanity check that the port scan picks up the correct open ports)
		*Likely will need to turn off the firewall on the target to get this to work.
	
	
