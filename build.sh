#!/usr/bin/env bash
# exit on error
set -o errexit

# Install nmap
apt-get update && apt-get install -y nmap

# Install Python dependencies
pip install -r requirements.txt