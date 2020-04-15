#!/bin/bash

while [ 1 ] ; do
	iperf3 -c firewall -t 60 -b 200 &
	iperf3 -c 10.0.0.1 -t 60 -b 200 -p 5202 &
	curl -s 10.0.0.1:443
done
