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

RestoreSettingFile = "./plugins/db-restore/settings.txt"
DatabaseLocation = "./database.db"
BackupDatabaseLocation = "./plugins/db-restore/default_settings.db"
BackupBackupDatabaseLocation = "./plugins/db-restore/default_settings.old"

class setting_restore():
    def __init__(self, rhapi):
        self.restore_db(self)
        self._rhapi = rhapi

    def restore_db(self, args):
        try:
            f = open(RestoreSettingFile)
            f.close()
            self.database_backup()
            try:
                shutil.copy(BackupDatabaseLocation, DatabaseLocation)
                logging.info("Default database restored!")
            except:
                logging.warn("Unable to find / restore default database " + BackupDatabaseLocation)
        except:
            pass

    def database_backup(self):
        backup_filename = "./db_bkp/auto_db_backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".db"
        try:
            shutil.copy(DatabaseLocation, backup_filename)
            logging.info("Database backed up to " + backup_filename)
        except:
            logging.warn("Unable to find / restore the database " + DatabaseLocation)


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
            shutil.copy(BackupDatabaseLocation, BackupBackupDatabaseLocation)
        except:
            logging.warn("Backup Database does not already exsist " + BackupDatabaseLocation)
        try:
            shutil.copy(DatabaseLocation, BackupDatabaseLocation)
            self._rhapi.ui.message_notify("Default startup database updated")
        except:
            logging.warn("Unable to find / restore the database " + DatabaseLocation)
        print("Database back up complete")

    def set_enabled_state(self, args):
        enabled_state = self._rhapi.db.option("restore_enabled_state")
        if enabled_state == '1':
            f = open(RestoreSettingFile, "w")
            f.write("enabled")
            f.close()
            logger.info("Settings restore file created")
            self._rhapi.ui.message_notify("Database restore is enabled at startup")
        else:
            if os.path.exists(RestoreSettingFile):
                os.remove(RestoreSettingFile)
                logger.info("Settings restore file removed")
                self._rhapi.ui.message_notify("Database restore is disabled at startup")

def initialize(rhapi):
    restore = setting_restore(rhapi)
    rhapi.ui.register_panel('setting_restore', 'Settings Restore', 'settings', order=0)
    rhapi.fields.register_option(UIField('restore_clear_races', 'Clear Races', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_clear_heats', 'Clear Heats', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_clear_classes', 'Clear Classes', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.ui.register_quickbutton('setting_restore', 'Prepare_db', 'Update Default Database', restore.prepare_db)
    rhapi.fields.register_option(UIField('restore_enabled_state', 'Enabled', UIFieldType.CHECKBOX, 0, 'Enable the settings restore at boot up (make sure to click save)'), 'setting_restore')
    rhapi.ui.register_quickbutton('setting_restore', 'save_settings', 'Save Enabled State', restore.set_enabled_state)
