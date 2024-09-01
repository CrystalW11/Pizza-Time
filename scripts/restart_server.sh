#!/bin/bash

# Navigate to the project directory
cd /home/ec2-user/pizza-time || exit

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install gunicorn if not already installed
pip show gunicorn > /dev/null 2>&1 || pip install gunicorn

# Stop any existing Gunicorn process
pkill gunicorn

# Start Gunicorn to serve the app, with logging
gunicorn --bind 0.0.0.0:80 wsgi:app --access-logfile /home/ec2-user/pizza-time/logs/access.log --error-logfile /home/ec2-user/pizza-time/logs/error.log

# Check if Gunicorn started successfully
if [ $? -ne 0 ]; then
  echo "Failed to start Gunicorn. Check logs for details."
  exit 1
fi

echo "Gunicorn started successfully."
