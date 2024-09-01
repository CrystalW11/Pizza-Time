#!/bin/bash

# Navigate to the project directory
cd /home/ec2-user/pizza-time || exit

# Activate the virtual environment
source venv/bin/activate

# Stop any existing Gunicorn process
sudo pkill gunicorn

# Start Gunicorn to serve the app with sudo
sudo gunicorn --bind 0.0.0.0:80 wsgi:app

# Check if Gunicorn started successfully
if [ $? -ne 0 ]; then
  echo "Failed to start Gunicorn. Check logs for details."
  exit 1
fi

echo "Gunicorn started successfully."
