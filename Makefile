all:

DIR=$(shell pwd -P)
PIPENV=python3 -m pipenv
BIN=/usr/bin/mkri

.PHONY: doc
doc:
	cd doc && make
	cp doc/projekt.pdf skupina_9.pdf

pipenv:
	$(PIPENV) install
	
runserver:
	$(PIPENV) run mkrifirewall/manage.py runserver

clean:
	cd doc && make clean
	rm skupina_9.pdf

install-dependencies:
	dnf -y install python3-pip make
	dnf -y install nftables
	pip3 install pip pipenv -U

add-bin:
	@echo '#!/bin/bash \
	cd $(DIR) \
	$(PIPENV) run mkrifirewall/manage.py runserver 0.0.0.0:80 \
	' | sed 's/\\//g' > $(BIN) 
	chmod +x $(BIN)

deploy:
	make install-dependencies
	make pipenv
	make add-bin
	cp mkri.service /etc/systemd/system/
	systemctl enable mkri.service
	systemctl start mkri.service
	nft -f mkrifirewall/firewall/sys_utils/config/default-io-chain-accept-all-counter.rules

zip:
	git archive HEAD -o skupina_9.zip

