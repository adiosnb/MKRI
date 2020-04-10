# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # config.vm.box = "generic/fedora31"
  config.vm.box = "centos/8"

  # config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provider "libvirt" do |lv|
    lv.memory = "2048"
    lv.cpus = "4"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo su
    # dnf -y update
    dnf -y install python3-pip make
    dnf -y install nftables
    pip3 install pip pipenv -U
    cd /vagrant
    python3 -m pipenv install
    cp /vagrant/mkri.service /etc/systemd/system/
    systemctl enable mkri.service
    systemctl start mkri.service
    exit
  SHELL
    # python3 -m pipenv run python mkrifirewall/manage.py runserver
end
