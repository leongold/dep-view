#!/bin/sh
docker volume create --name=db_volume_a_i || { echo 'failed to create volume a-i'; exit 1; }
docker volume create --name=db_volume_j_q || { echo 'failed to create volume j-q'; exit 1; }
docker volume create --name=db_volume_r_z || { echo 'failed to create volume r-z'; exit 1; }

