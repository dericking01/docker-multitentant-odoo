#!/bin/bash

set -e  # Exit immediately if any command fails

echo "Pulling the latest Portainer image..."
docker pull portainer/portainer-ce:latest || { echo "Failed to pull Portainer image"; exit 1; }

echo "Creating Docker volume for Portainer data..."
docker volume create portainer_data || { echo "Failed to create volume"; exit 1; }

echo "Running the Portainer container..."
docker run -d -p 9000:9000 -p 9443:9443 --name portainer \
--restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v portainer_data:/data \
portainer/portainer-ce:latest || { echo "Failed to run Portainer container"; exit 1; }

echo "Portainer has been successfully deployed!"