#!/bin/bash

# Update package lists
sudo apt update

# Install Docker
### to remove packages first "for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done"
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG root ubuntu
sudo usermod -aG sudo ubuntu

# Install btop
sudo apt install -y btop

# Add oracle opc user to root group
sudo usermod -aG root opc

# Set up aliases
echo 'alias d="docker"' >> ~/.bashrc

# Reload bash to apply changes
source ~/.bashrc

echo "Setup complete."
