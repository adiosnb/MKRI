# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/8"


  config.vm.provider "libvirt" do |lv|
    lv.memory = "2048"
    lv.cpus = "2"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo dnf -y install iperf3 vim
    iperf3 -sD
    iperf3 -sD -p 5202
    sudo sh /vagrant/add_tunnel.sh
  SHELL

  config.vm.define "generator" do |gen|
    gen.vm.hostname = "generator"
    gen.vm.provision "shell", inline: <<-SHELL
      sudo cp /vagrant/generator.sh /usr/bin/mkri_generator
      sudo cp /vagrant/generator.service /etc/systemd/system
      systemctl enable generator
      systemctl start generator
      ipsec auto --up tun1
      ip addr add 10.0.0.2/24 dev eth0
    SHELL
  end

  config.vm.define "firewall" do |fw|
    fw.vm.hostname = "firewall"
    fw.vm.network "forwarded_port", guest: 80, host: 8000
    fw.vm.provision "shell", inline: <<-SHELL
      cd /vagrant
      sudo dnf -y install make
      sudo make deploy
      ip addr add 10.0.0.1/24 dev eth0
    SHELL

  end

end
