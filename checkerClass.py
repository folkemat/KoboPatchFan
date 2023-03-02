#Filename: CheckerClass.py
# If available, the file kobopatch.yaml (which comes from the patch.zip file) 
#is used to read out the firmware for which the patch is intended (via version:). 
#This information should then be displayed to the user

import yaml
import os
from configSettingsClass import configSettings

class checkerClass:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        self.patchVersion = "Unknown"

    def readKobopatchyaml(self):
        path = str(configSettings(self._settings).app_folder)
        kobopatch_file_path = os.path.join(path, "kobopatch.yaml")
        #Processing the patch file
        try:
            if not os.path.isfile(kobopatch_file_path):
                configSettings.log(self, "Error Checker 1: Can not read kobopatch.yaml file!")
                return "Not found - click 'Start' to begin!"
        
            with open(kobopatch_file_path, encoding='utf-8') as stream:
                data = yaml.safe_load(stream)

            version = data.get("version")
            if version is not None:
                self.patchVersion = str(version)
            else:
                configSettings.log(self, "Error Checker: Can not read version of kobopatch.yaml file")
                return "Not found - click 'Start' to begin!"
            
            return self.patchVersion
 
        except Exception as e:
            configSettings.log(self, "Error Checker 2: Can not read kobopatch.yaml file!: "+str(e))
            return "Not found - click 'Start' to begin!"