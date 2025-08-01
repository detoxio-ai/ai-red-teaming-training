#!/bin/bash

set -e

# === Config ===
VNC_PASSWORD="${VNC_PASSWORD:-MySecureVNCpass}"
VNC_DISPLAY=":1"
SCREEN_RESOLUTION="1024x768x16"

export DEBIAN_FRONTEND=noninteractive

echo "[+] Installing desktop environment and VNC tools..."
sudo apt update
sudo apt install -y x11vnc xvfb lxde-core lxterminal

echo "[+] Setting VNC password..."
mkdir -p ~/.vnc
x11vnc -storepasswd "$VNC_PASSWORD" ~/.vnc/passwd

echo "[+] Creating Xvfb virtual display ($VNC_DISPLAY)..."
Xvfb $VNC_DISPLAY -screen 0 $SCREEN_RESOLUTION &

sleep 2

echo "[+] Launching LXDE desktop in background..."
DISPLAY=$VNC_DISPLAY startlxde &

sleep 5

echo "[+] Starting x11vnc on $VNC_DISPLAY..."
x11vnc -display $VNC_DISPLAY -rfbauth ~/.vnc/passwd -forever -bg

echo "[+] Allowing VNC port 5900 through firewall..."
sudo ufw allow 5900/tcp || true

echo "=================================================================="
echo " ✅ Headless VNC Desktop is running!"
echo " 🔐 Password: $VNC_PASSWORD"
echo " 🖥️  Desktop: LXDE on $VNC_DISPLAY"
echo " 🌐 Accessible via: VNC or Apache Guacamole"
echo "=================================================================="

