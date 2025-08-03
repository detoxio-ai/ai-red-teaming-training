#!/bin/bash
set -e

if [[ -z "$DTX_PASSWORD" ]]; then
  echo "ERROR: Please set the DTX_PASSWORD environment variable."
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

# Disable interactive restart prompts (fixes lingering packagekit.service prompt)
echo "\$nrconf{restart} = 'a';" | sudo tee /etc/needrestart/conf.d/disable-prompt.conf >/dev/null

# Update and upgrade packages
sudo apt update
sudo apt upgrade -y

# Install desktop and XRDP
sudo apt install -y xfce4 xfce4-goodies xrdp

# Configure XRDP
echo "startxfce4" | sudo tee /etc/skel/.xsession >/dev/null
echo "startxfce4" > /home/dtx/.xsession
sudo chown dtx:dtx /home/dtx/.xsession
sudo chmod +x /home/dtx/.xsession

sudo adduser xrdp ssl-cert
sudo systemctl enable xrdp
sudo systemctl restart xrdp

# Set password for user
echo "dtx:$DTX_PASSWORD" | sudo chpasswd
