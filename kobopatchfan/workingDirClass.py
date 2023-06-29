#Filename: workingDirClass.py
import os
import sys
import subprocess
from PyQt6.QtCore import QDir, QFileInfo
from configSettingsClass import configSettings

class WorkingDir:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view

    def checkForFolder(self):
        
        #create working folder:
        working_dir = str(configSettings(self._settings).documents_folder)
        working_folder_name = str(configSettings(self._settings).working_folder)
        app_folder = str(configSettings(self._settings).app_folder)

        if not os.path.exists(app_folder):
            try:
                app_folder = QDir(working_dir).mkdir(working_folder_name)
            except Exception as e:
                configSettings.log(self, "Error: Could not create working dir folder: "+str(e))
                self._view.tab_widget.working_dir_plainTextEdit.setPlainText("Error: Could not create working dir folder: "+str(e))
                return

        abs_path = QDir(working_dir).filePath(working_folder_name)
        self._view.tab_widget.working_dir_plainTextEdit.setPlainText(str(abs_path))

    def openWorkingFolder(self):
        try:
            app_folder = str(configSettings(self._settings).app_folder)
            if sys.platform == "win32":
                os.startfile(app_folder)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, app_folder])
        except Exception as e:
            configSettings.log(self, "Error: Could not open working dir folder")
