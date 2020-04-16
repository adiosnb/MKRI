#!/bin/bash

while [ 1 ] ; do
	iperf3 -c firewall -t 60 -b 1M &
	iperf3 -c 10.0.0.1 -t 60 -b 1M -p 5202 &
	ping 10.0.0.1 -i 0.4 -s 32000 -c 150 &
	for i in $(seq 60); do 
		ssh -o "StrictHostKeyChecking=no" 10.0.0.1 cat /boot/config*
		sleep 0.7
	done
	wait
done
