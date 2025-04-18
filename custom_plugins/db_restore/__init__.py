'''Settings restore'''

import logging
import os
import shutil
import time
import datetime
logger = logging.getLogger(__name__)
from dataclasses import dataclass, asdict 
from eventmanager import Evt
from EventActions import ActionEffect
from RHUI import UIField, UIFieldType, UIFieldSelectOption


class setting_restore():
    def __init__(self, rhapi):
        self._rhapi = rhapi
        if (self._rhapi.API_VERSION_MAJOR <= 1 and self._rhapi.API_VERSION_MINOR <= 2):
            self.user_data_location = "."
        else:
            self.user_data_location = self._rhapi.server.data_dir

        self.RestoreSettingFile = self.user_data_location + "/plugins/db_restore/settings.txt"
        self.DatabaseLocation = self.user_data_location + "/database.db"
        self.BackupDatabaseLocation = self.user_data_location + "/plugins/db_restore/default_settings.db"
        self.BackupBackupDatabaseLocation = self.user_data_location + "/plugins/db_restore/default_settings.old"
        self.DbBackupDir = self.user_data_location + "/db_bkp"

        if not os.path.exists(self.DbBackupDir):
            os.makedirs(self.DbBackupDir)
            logging.info(f"Created directory: {self.DbBackupDir}")
            
        self.restore_db(self)

    def restore_db(self, args):
        try:
            with open(self.RestoreSettingFile, 'r') as file:
                data = file.readlines()

            if time.time() > float(data[2]):
                self.database_backup()
                try:
                    shutil.copy(self.BackupDatabaseLocation, self.DatabaseLocation)
                    logging.info("Default database restored!")
                except:
                    logging.warn("Unable to find / restore default database " + self.BackupDatabaseLocation)
            else:
                logging.info("Default database not restored - time since last boot not great enough!")

            data[2] = str(time.time() + float(data[1])) + '\n'

            with open(self.RestoreSettingFile, 'w') as file:
                file.writelines( data )
            file.close()
        except:
            pass

    def database_backup(self):
        backup_filename = self.DbBackupDir + "/auto_db_backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".db"
        try:
            shutil.copy(self.DatabaseLocation, backup_filename)
            logging.info("Database backed up to " + backup_filename)
        except:
            logging.warn("Unable to backup the database " + self.DatabaseLocation)


    def prepare_db(self, args):
        self._rhapi.ui.message_notify("Database backup started, please wait for confirmation before leaving the page!")
        self._rhapi.race.clear()
        self.database_backup()    
        if self._rhapi.db.option("restore_clear_races") == '1':
            self._rhapi.db.races_clear()
            while (len(self._rhapi.db.races) != 0):
                pass
        if self._rhapi.db.option("restore_clear_heats") == '1':
            self._rhapi.db.heats_reset()
            while (len(self._rhapi.db.heats) != 0):
                pass
        if self._rhapi.db.option("restore_clear_classes") == '1':
            self._rhapi.db.raceclasses_reset()
            while (len(self._rhapi.db.raceclasses) != 0):
                pass

        time.sleep(1)
        try:
            shutil.copy(self.BackupDatabaseLocation, self.BackupBackupDatabaseLocation)
        except:
            logging.warn("Backup Database does not already exsist " + self.BackupDatabaseLocation)
        try:
            shutil.copy(self.DatabaseLocation, self.BackupDatabaseLocation)
            self._rhapi.ui.message_notify("Default startup database updated")
        except:
            logging.warn("Unable to find / restore the database " + self.DatabaseLocation)
        print("Database back up complete")

    def set_enabled_state(self, args):
        enabled_state = self._rhapi.db.option("restore_enabled_state")
        restore_wait_time = self._rhapi.db.option("restore_wait_time")
        if enabled_state == '1':
            data = ["enabled\n", str(int(restore_wait_time) * 60) + '\n', str(time.time() + (float(restore_wait_time) * 60)) + '\n']
            with open(self.RestoreSettingFile, 'w') as f:
                f.writelines( data )
            f.close()
            logger.info("Settings restore file created")
            self._rhapi.ui.message_notify("Database restore is enabled at startup")
        else:
            if os.path.exists(self.RestoreSettingFile):
                os.remove(self.RestoreSettingFile)
                logger.info("Settings restore file removed")
                self._rhapi.ui.message_notify("Database restore is disabled at startup")

    def get_file_settins(self):
        settings = {
        "enabled": 0,
        "wait_time": 0
        }
        try:
            with open(self.RestoreSettingFile, 'r') as file:
                data = file.readlines()
            if data[0] == "enabled\n":
                settings["enabled"] = 1
            settings["wait_time"] = int(int(data[1]) / 60)
        except:
            pass
        return settings

def initialize(rhapi):
    restore = setting_restore(rhapi)
    rhapi.ui.register_panel('setting_restore', 'Settings Restore', 'settings', order=0)
    rhapi.fields.register_option(UIField('restore_clear_races', 'Clear Races', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_clear_heats', 'Clear Heats', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_clear_classes', 'Clear Classes', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.ui.register_quickbutton('setting_restore', 'Prepare_db', 'Update Default Database', restore.prepare_db)
    settings = restore.get_file_settins()
    rhapi.fields.register_option(UIField('restore_wait_time', 'Restore Wait Time', UIFieldType.TEXT, str(settings["wait_time"]), 'Time in mins that must be exceeded since last boot to reset the database (make sure to click save)'), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_enabled_state', 'Enabled', UIFieldType.CHECKBOX, settings["enabled"], 'Enable the settings restore at boot up (make sure to click save)'), 'setting_restore')
    rhapi.ui.register_quickbutton('setting_restore', 'save_settings', 'Save', restore.set_enabled_state)
