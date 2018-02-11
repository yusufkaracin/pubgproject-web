# -*- mode: ruby -*-
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.synced_folder ".", "/home/vagrant/project"
  config.vm.hostname = "pubgproject-dev"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "pubgproject-dev"
    vb.memory = "1024"
  end

  config.vm.provision "increase_swap", type: "shell", path: "utility/increase_swap.sh"
  config.vm.provision "install_os_dependencies", type: "shell", path: "utility/install_os_dependencies.sh"
  config.vm.provision "install_redis", type: "shell", path: "utility/install_redis.sh"
  config.vm.provision "prepare_venv", type: "shell", path: "utility/prepare_venv.sh", privileged: false

end
