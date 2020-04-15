#!/bin/bash

while [ 1 ] ; do
	iperf3 -c firewall -t 60 -b 1M &
	iperf3 -c 10.0.0.1 -t 60 -b 1M -p 5202
	curl -s 10.0.0.1:443
done
