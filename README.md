# RotorHazard Automatic Database Restore
This plugin for [RotorHazard](https://github.com/RotorHazard/RotorHazard) lets you restore a default database when the server boots up. This is useful if multiple people use your timer and you want it to be in a known state after someone else has used it.

# How to Install
Run the following command in the SSH terminal to install the settings restore 
```
cd ~
wget https://github.com/Aaronsss/RH-Settings-Restore/archive/refs/heads/main.zip
unzip ./main.zip
rm -R ~/RotorHazard/src/server/plugins/db-restore
mv ~/RH-Settings-Restore-main/db-restore/ ~/RotorHazard/src/server/plugins/
rm -R ./RH-Settings-Restore-main/
rm ./main.zip
sudo systemctl restart rotorhazard.service
```

If you wish to install manually, place the db-restore folder within the RotorHazard plugins folder Rotorhazard/src/server/plugins then start / restart the server  

# How to setup

Go to Settings -> Settings Restore tab 
1. Clear Races - Clears the Races when the update Defult Database button is clicked
2. Clear Heats - Clears the Heats when the update Defult Database button is clicked
3. Clear Classes - Clears the classes when the update Defult Database button is clicked
4. Enabled - This tick box selects if the plugin is active at server start up or not
5. Update Default Database - When clicked the 3 clear options above are completed and the database is copied to the default database location
6. Save Enabled State - saves the state of the enabled check box to a file so it can be checked at start up (before the servers database is initialised) 

