#!/bin/bash
set -e

# Log file
mkdir -p -m 700 /logs
LOGFILE="./logs/setup.log"

# Create venv
echo "Creating virtual environment '.venv'..."

# Check for existing virtual environment
if [ -d ".venv" ]; then
  echo "Using existing virtual environment '.venv'..."
else
  echo "Creating virtual environment '.venv'..."
  python3 -m venv .venv
fi

# Activate and install
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Log completion
echo "Setup completed successfully on $(date)"
