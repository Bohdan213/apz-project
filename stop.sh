#!/bin/bash

# Stop and remove containers
docker stop consul-dev node-1 node-2 apz-project-postgres mongo1 mongo2 >/dev/null 2>&1
docker rm consul-dev node-1 node-2 apz-project-postgres mongo1 mongo2 >/dev/null 2>&1

echo "Services stopped successfully."
