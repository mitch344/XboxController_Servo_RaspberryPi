#!/bin/bash

SERVICE_FILE="/etc/systemd/system/new_script.service"

# Stop the service
sudo systemctl stop new_script.service

# Disable the service to prevent it from starting at boot
sudo systemctl disable new_script.service

# Remove the service file
sudo rm -f $SERVICE_FILE

# Reload systemd to apply changes
sudo systemctl daemon-reload

echo "Service uninstalled successfully."
