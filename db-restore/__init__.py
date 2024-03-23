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
        self.database_backup()
        shutil.copy(BackupDatabaseLocation, DatabaseLocation)
        logging.info("Default database restored!")

    def database_backup(self, args):
        backup_filename = "./db_bkp/auto_db_backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".db"
        shutil.copy(DatabaseLocation, backup_filename)
        logging.info("Database backed up to " + backup_filename)

    def prepare_db(self, args):
        self._rhapi.race.clear()
        self.database_backup()    
        if self._rhapi.db.option("restore_clear_races") == '1':
            self._rhapi.db.races_clear()
        if self._rhapi.db.option("restore_clear_heats") == '1':
            self._rhapi.db.heats_reset()
        if self._rhapi.db.option("restore_clear_classes") == '1':
            self._rhapi.db.raceclasses_reset()

        time.sleep(5)
        shutil.copy(BackupDatabaseLocation, BackupBackupDatabaseLocation)
        shutil.copy(DatabaseLocation, BackupDatabaseLocation)
        print("Database generated")

    def set_enabled_state(self, args):
        enabled_state = self._rhapi.db.option("restore_enabled_state")
        if enabled_state == '1':
            f = open(RestoreSettingFile, "w")
            f.write("enabled")
            f.close()
            logger.info("Settings restore file created")
        else:
            if os.path.exists(RestoreSettingFile):
                os.remove(RestoreSettingFile)
                logger.info("Settings restore file removed")

def initialize(rhapi):
    restore = setting_restore(rhapi)
    rhapi.ui.register_panel('setting_restore', 'Settings Restore', 'settings', order=0)
    rhapi.fields.register_option(UIField('restore_clear_races', 'Clear Races', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_clear_heats', 'Clear Heats', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.fields.register_option(UIField('restore_clear_classes', 'Clear Classes', UIFieldType.CHECKBOX), 'setting_restore')
    rhapi.ui.register_quickbutton('setting_restore', 'Prepare_db', 'Update Default Database', restore.prepare_db)
    rhapi.fields.register_option(UIField('restore_enabled_state', 'Enabled', UIFieldType.CHECKBOX, 0, 'Enable the settings restore at boot up (make sure to click save)'), 'setting_restore')
    rhapi.ui.register_quickbutton('setting_restore', 'save_settings', 'Save Enabled State', restore.set_enabled_state)