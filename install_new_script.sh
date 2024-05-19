#!/bin/bash

SERVICE_FILE="/etc/systemd/system/new_script.service"
PYTHON_PATH="/usr/bin/python3"
SCRIPT_PATH="/home/pi/new.py"

# Create the systemd service file
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Run new.py at startup
After=multi-user.target

[Service]
Type=simple
ExecStart=$PYTHON_PATH $SCRIPT_PATH
WorkingDirectory=$(dirname $SCRIPT_PATH)
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start at boot
sudo systemctl enable new_script.service

# Start the service immediately
sudo systemctl start new_script.service

echo "Service installed and started successfully."
