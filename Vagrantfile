# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'etc'
require 'pathname'

Vagrant.configure("2") do |config|
    # define synced folders
    config.vm.synced_folder ".", "/home/vagrant/pubmed-ingester"

    config.vm.define "pubmed_ingester" do |pubmed_ingester|
        # define virtualization provider
        pubmed_ingester.vm.provider "virtualbox"
        # define box
        pubmed_ingester.vm.box = "bento/ubuntu-16.04"

        config.vm.provider "virtualbox" do |v|
            # define RAM in MBs
            v.memory = 2048
            # define number of vCPUs
            v.cpus = 2
        end
    end

    # forward SSH agent
    config.ssh.forward_agent = true
    config.ssh.insert_key = false

    config.vm.network :forwarded_port, guest: 22, host: 2401, id: "ssh", auto_correct: false
    config.vm.network :forwarded_port, guest: 5432, host: 5432, id: "postgres"

    # provision with Ansible
    config.vm.provision :ansible do |ansible|
        ansible.playbook = "app-pubmed-ingester.yaml"
        ansible.host_key_checking = false
        ansible.vault_password_file = ".ansible-vault-password"

        if ENV['ANSIBLE_TAGS'] != ""
            ansible.tags = ENV['ANSIBLE_TAGS']
        end

        ansible.extra_vars = {
            "app_pubmed_ingester"=> {is_vagrant: true},
        }
    end
end
