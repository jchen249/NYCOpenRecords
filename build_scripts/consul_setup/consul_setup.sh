#!/usr/bin/env bash

# Install Consul binaries
cd /tmp/
wget https://releases.hashicorp.com/consul/1.0.0/consul_1.0.0_linux_amd64.zip?_ga=2.225939090.948864614.1509545805-1112607485.1509545805
unzip consul_1.0.0_linux_amd64.zip
sudo mv consul /bin/

# Start Consul server
sudo consul agent -server -bootstrap -data-dir /tmp/consul -bind 10.0.0.5 -ui