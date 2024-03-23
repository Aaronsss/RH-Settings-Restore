#!/bin/bash

# Script to update the default database for rotorhazard at boot

sudo systemctl stop rotorhazard.service
cp ~/RH-Settings-Restore/database.db ~/RH-Settings-Restore/database.old
cp ~/RotorHazard/src/server/database.db ~/RH-Settings-Restore/database.db 
sudo systemctl start rotorhazard.service

echo "Default Rotorhazard database updated"