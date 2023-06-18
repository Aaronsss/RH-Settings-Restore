FILE=/home/sgdc/RotorHazard/src/server/db_bkp/default_settings.db

cd ~
if [ -f "$FILE" ]; then
    echo "$(date) Default DB settings exsist already"
else 
    cp ~/RH-Settings-Restore/default_settings.db $FILE
    chmod 644 $FILE

    echo "$(date) Copying default DB to DB backup folder"

fi