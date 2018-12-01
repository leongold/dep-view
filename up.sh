#!/bin/sh
docker-compose up || { echo 'failed to run'; exit 1; }
