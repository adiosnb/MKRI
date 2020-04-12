#!/bin/bash

while [ 1 ] ; do
	iperf3 -c firewall -t 60 -b 10M &
	iperf3 -c 10.0.0.1 -t 60 -b 10M -p 5202
done
