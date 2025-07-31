# === Install Metasploit ===
sudo -u $USER bash -c 'bash -lc "
  curl -sSL https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
  chmod 755 msfinstall
  sudo rm -f /usr/share/keyrings/metasploit-framework.gpg
  yes | ./msfinstall > /dev/null 2>&1 || true
  yes | msfdb init > /dev/null 2>&1 || true
"'