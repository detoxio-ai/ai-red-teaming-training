#!/bin/bash

# Exit on error
set -e

# Ensure the DTX_PASSWORD environment variable is set
if [[ -z "$DTX_PASSWORD" ]]; then
  echo "ERROR: Please set the DTX_PASSWORD environment variable."
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

# Suppress daemon restart prompts during upgrade
echo '* libraries/restart-without-asking boolean true' | sudo debconf-set-selections

# Update and upgrade packages
sudo apt update
sudo apt upgrade -y

# Install Xfce (lightweight desktop)
sudo apt install -y xfce4 xfce4-goodies

# Install XRDP (remote desktop protocol server)
sudo apt install -y xrdp

# Set Xfce as the default desktop for XRDP sessions
echo "startxfce4" | sudo tee /etc/skel/.xsession >/dev/null
echo "startxfce4" > /home/dtx/.xsession
sudo chown dtx:dtx /home/dtx/.xsession
sudo chmod +x /home/dtx/.xsession

# Add xrdp user to the ssl-cert group (needed for encryption)
sudo adduser xrdp ssl-cert

# Enable and start the XRDP service
sudo systemctl enable xrdp
sudo systemctl restart xrdp

# Set the password for user 'dtx'
echo "dtx:$DTX_PASSWORD" | sudo chpasswd

echo "✅ XRDP setup complete. You can now connect via RDP."
