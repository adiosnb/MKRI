#!/bin/bash

dnf -y install libreswan bind-utils

LEFT=$(dig +short firewall)
RIGHT=$(dig +short generator)

DIR=/etc/ipsec.d

echo "$LEFT $RIGHT : PSK \"OTigys4KTfE4cAkE1P9ku1iEYqCA\" " > $DIR/tun1.secrets

cat > $DIR/tun1.conf << EOF
conn tun1
	type=transport
	connaddrfamily=IPv4
	authby=secret
	left=$LEFT
	right=$RIGHT
	phase2=esp
	phase2alg=aes128-sha1
	keyexchange=ike
	pfs=yes
	auto=start
	encapsulation=no
EOF

systemctl enable ipsec 
systemctl start ipsec 
ipsec auto --add tun1

