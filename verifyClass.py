#Filename: verifyClass.py

import os
import json
from configSettingsClass import configSettings
import re

class verifyDownload:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        
    def verifyConfig(self, index):
        try:
            configSettings.log(self, "Check for matching version ...")
            foundMatch = False
            allPatchVersions = self.parsePatchJson()
            if len(allPatchVersions) == 0:
                configSettings.log(self, "Error: Could not find any patches")
                return
            choosenFirmware = configSettings.getSetting(self, "kobo_this_version")
            for version in allPatchVersions:
                if version == choosenFirmware:
                    foundMatch = True
                    break
                else:
                    foundMatch = False
                    pass        
            if foundMatch:
                configSettings.log(self, "Found a match for "+choosenFirmware+"="+version)
                self._view.tab_widget.labelVerifyResult.setText("Found patch for firmware "+choosenFirmware)
                self._view.tab_widget.labelVerifyResult.setStyleSheet('color:green; font-weight:bold')
            else:
                configSettings.log(self, "Found NO match for "+choosenFirmware)
                self._view.tab_widget.labelVerifyResult.setText("Found no patch for firmware "+choosenFirmware)
                self._view.tab_widget.labelVerifyResult.setStyleSheet('color:red; font-weight:bold')

            configSettings.log(self, "Status Verify: Success and done")
        except:
            configSettings.log(self, "Status Verify: Error verifying configuration")

    def parsePatchJson(self):
        path = str(configSettings.getSetting(self, "working_dir"))
        filename = "patches.json"
        file_path = os.path.join(path, filename)
        versionList = []
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                json_object = json.loads(file_content)
            for elements in json_object["assets"]:
                thisVersion = elements["name"]
                thisVersion = thisVersion.replace(".zip", "")           
                thisVersion = re.sub('[^\d\.]', '', thisVersion)
                versionList.append(thisVersion)
            configSettings.log(self, "Successfully parsed patches.json")
        except Exception as e:
            configSettings.log(self, "Error parsing patches.json: "+str(e))
        return versionList

    def verifyFirmwarePatch(self, index):
        self.verifyConfig(index)