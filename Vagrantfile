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
    cd /vagrant
    sudo dnf -y install make
    sudo make deploy
  SHELL

end
