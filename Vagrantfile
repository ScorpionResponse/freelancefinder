# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  # Expose on the network
  config.vm.hostname = "freelancebox.local"

  config.ssh.forward_agent = true

  # Define the DB machines
  config.vm.define "freelance_db1" do |instance|
    instance.vm.network "private_network", ip: "192.168.2.4"
    config.vm.provider "virtualbox" do |v|
      v.name = "freelance_db1"
      v.memory = 1024
      v.cpus = 1
    end
  end

  # Define the App machines
  config.vm.define "freelance_app1" do |instance|
    instance.vm.network "private_network", ip: "192.168.2.3"
    config.vm.provider "virtualbox" do |v|
      v.name = "freelance_app1"
      v.memory = 1024
      v.cpus = 1
    end
  end

  # Define the control machine
  config.vm.define "freelance_control", primary: true do |instance|
    instance.vm.network "private_network", ip: "192.168.2.2"
    instance.vm.provider "virtualbox" do |v|
      v.name = "freelance_control"
      v.memory = 1024
      v.cpus = 1
    end

    # Copy the ansible provisioning info over to the local (not shared) drive
    $script = <<SCRIPT
mkdir provisioning
cp -r /vagrant/ansible_vagrant provisioning/ansible
SCRIPT
  
    config.vm.provision :shell, privileged: false, inline: $script
  
    # provision the rest with ansible
    config.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/control.yml"
      ansible.galaxy_role_file = "ansible/roles.yml"
      ansible.provisioning_path = "/home/ubuntu/provisioning"
      ansible.verbose = "v"
    end
  end

  # Define the build machine
  config.vm.define "freelance_build" do |instance|
    instance.vm.network "private_network", ip: "192.168.2.5"
    instance.vm.provider "virtualbox" do |v|
      v.name = "freelance_build"
      v.memory = 1024
      v.cpus = 1
    end

    # Copy the ansible provisioning info over to the local (not shared) drive
    $script = <<SCRIPT
mkdir provisioning
cp -r /vagrant/ansible_vagrant provisioning/ansible
SCRIPT
  
    config.vm.provision :shell, privileged: false, inline: $script
  
    # provision the rest with ansible
    config.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/build.yml"
      ansible.galaxy_role_file = "ansible/roles.yml"
      ansible.provisioning_path = "/home/ubuntu/provisioning"
      ansible.verbose = "v"
    end
  end

  # Set the root password
  $root_script = <<SCRIPT2
echo "ubuntu:vagrant" | chpasswd > /dev/null 2>&1
SCRIPT2

  config.vm.provision :shell, privileged: true, inline: $root_script
end
