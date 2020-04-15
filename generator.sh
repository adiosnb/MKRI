#!/bin/bash

while [ 1 ] ; do
	iperf3 -c firewall -t 60 -b 1M &
	iperf3 -c 10.0.0.1 -t 60 -b 1M -p 5202 &
	for i in $(seq 120); do 
		ssh -o "StrictHostKeyChecking=no" 10.0.0.1 find /
		ssh -o "StrictHostKeyChecking=no" 10.0.0.1 cat /var/log/*
		sleep 0.5
	done
done
