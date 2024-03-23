#!/usr/bin/env bash
set -e # Exit immediately if a command exits with a non-zero status

if [ "$(id -u)" -eq 0 ]; then
    echo "Run me as normal user, not root!"
    exit 1
fi

echo "Cloning repo..."
# This installation script will prefer cloning by ssh if it is setup on the client machine
# Check for presence of common SSH key names
ssh_dir="$HOME/.ssh"
keys=( "id_rsa" "id_ed25519" "id_dsa" "id_ecdsa" )

found=false
for key in ${keys[@]}; do
  if [[ -d $ssh_dir && -f "$ssh_dir/$key" ]]; then
    found=true
    echo "SSH key found. Cloning with SSH..." 
    git clone git@github.com:cdf144/bookstore-web-app.git && break
  fi
done

# Fallback to HTTPS if SSH key check fails
if [[ $found = false ]]; then
  echo "SSH key not found. Cloning with HTTPS..."
  git clone https://github.com/cdf144/bookstore-web-app.git
fi

cd bookstore-web-app/

echo "Creating venv..."
python -m venv .venv
source .venv/bin/activate

echo "Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
