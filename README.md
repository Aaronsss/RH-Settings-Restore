# RotorHazard Automatic Database Restore
This plugin for [RotorHazard](https://github.com/RotorHazard/RotorHazard) lets you restore a default database when the server boots up. This is useful if multiple people use your timer and you want it to be in a known state after someone else has used it.

# How to Install
There are 3 ways you can install this plugin
1. Though RotorHazards community plugin manager on RotorHazard 4.3.0 or greater:  
   This can be found on your timer which must be connected to the internet by going to settings -> plugins -> Browse Community Plugins (online only) -> Utilities then install the Settings Restore plugin  
   
2. Paste the following commands into your timers SSH terminal:  
  You can also paste the below command into your command line to instal the plugin (your timer will need an internet connection)  
  ```
  cd ~
  wget https://github.com/Aaronsss/RH-Settings-Restore/archive/refs/heads/main.zip
  unzip ./main.zip
  rm -R ~/RotorHazard/src/server/plugins/db-restore
  rm -R ~/RotorHazard/src/server/plugins/db_restore
  mv ~/RH-Settings-Restore-main/custom_plugins/db_restore/ ~/RotorHazard/src/server/plugins/
  rm -R ./RH-Settings-Restore-main/
  rm ./main.zip
  sudo systemctl restart rotorhazard.service
  ```
3. Manually:  
  If you wish to install manually, place the custom_plugins/db_restore folder within the RotorHazard plugins folder Rotorhazard/src/server/plugins then start / restart the server  

# How to setup

Go to Settings -> Settings Restore tab 
1. Clear Races - Clears the Races when the update Defult Database button is clicked
2. Clear Heats - Clears the Heats when the update Defult Database button is clicked
3. Clear Classes - Clears the classes when the update Defult Database button is clicked
4. Enabled - This tick box selects if the plugin is active at server start up or not
5. Update Default Database - When clicked the 3 clear options above are completed and the database is copied to the default database location
6. Save Enabled State - saves the state of the enabled check box to a file so it can be checked at start up (before the servers database is initialised) 

