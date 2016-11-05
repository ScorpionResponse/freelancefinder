# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  # Expose on the network
  config.vm.hostname = "freelancebox.local"
  config.vm.network "forwarded_port", guest: 5005, host: 5005

  config.ssh.forward_agent = true

  # Copy the ansible provisioning info over to the local (not shared) drive
  $script = <<SCRIPT
mkdir provisioning
cp -r /vagrant/ansible provisioning/
SCRIPT

  config.vm.provision :shell, privileged: false, inline: $script

  # provision the rest with ansible
  config.vm.provision "ansible_local" do |ansible|
    #ansible.inventory_path = "ansible/vagrant"
    ansible.playbook = "ansible/playbook.yml"
    ansible.provisioning_path = "/home/ubuntu/provisioning"
    ansible.verbose = "v"
  end

  config.vm.provider "virtualbox" do |v|
    v.name = "freelancedev"
    v.memory = 1024
    v.cpus = 1
  end

end
