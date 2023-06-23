now="$(date +'%Y%m%d_%H%M%S')"
db_loc=~/RotorHazard/src/server/database.db
db_bkup=~/RotorHazard/src/server/db_bkp/database_$now.db

cp $db_loc $db_bkup
printf "$(date) Database backed up: $db_bkup \n"

cp ~/RH-Settings-Restore/database.db $db_loc
#chmod 644 $FILE

cd ~/RotorHazard/src/server
python server.py