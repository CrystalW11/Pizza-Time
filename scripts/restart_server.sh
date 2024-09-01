#!/bin/bash
cd /home/ec2-user/pizza-time
source venv/bin/activate
# Stop any existing Gunicorn process
pkill gunicorn
# Start Gunicorn to serve the app
gunicorn --bind 0.0.0.0:80 wsgi:app
