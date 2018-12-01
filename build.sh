#!/bin/sh
docker-compose build || { echo 'failed to build'; exit 1; }

