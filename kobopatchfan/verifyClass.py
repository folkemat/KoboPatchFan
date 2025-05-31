#Filename: verifyClass.py

import os
import json
from configSettingsClass import configSettings
from updateDbClass import updateDb
import re
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox

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
                self._view.tab_widget.labelVerifyResult.setText("Found patch for: "+choosenFirmware+"! Ready!")
                self._view.tab_widget.labelVerifyResult.setStyleSheet('color:green; font-weight:bold')
                self._view.tab_widget.checkbox_patch_anyway.hide()
                self._view.tab_widget.button_patch_anyway_help.hide()
                self._view.tab_widget.labelPatchAnywayResult.hide()
                #no need to override
                configSettings.setSetting(self, "override_kobo_this_version", "0.00.00000")
            else:
                configSettings.log(self, "Found NO match for "+choosenFirmware)
                self._view.tab_widget.labelVerifyResult.setText("Found no patch for: "+choosenFirmware)
                self._view.tab_widget.labelVerifyResult.setStyleSheet('color:red; font-weight:bold')
                self._view.tab_widget.checkbox_patch_anyway.show()
                self._view.tab_widget.button_patch_anyway_help.show()
                #try to find latest patch version, and override
                self.tryToFindLatestPatch(0)

            configSettings.log(self, "Status Verify: Success and done")
        except:
            configSettings.log(self, "Status Verify: Error verifying configuration")

    def parsePatchJson(self):
        path = str(configSettings(self._settings).app_folder)
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
        #another firmware version was chosen
        self._view.tab_widget.checkbox_patch_anyway.setChecked(False) #reset anyway-checkbox
        configSettings.setSetting(self, "override_kobo_this_version", "0.00.00000") #reset override
        self.verifyConfig(index) #check for patches

    def tryToPatchAnyway(self, index):
        configSettings.setSetting(self, "override_kobo_this_version", "0.00.00000") #reset override
        if self._view.tab_widget.checkbox_patch_anyway.isChecked() == True:
            foundMatch = self.tryToFindLatestPatch(0)[0]
            latestVersion = self.tryToFindLatestPatch(0)[1]
            if foundMatch:
                configSettings.setSetting(self, "override_kobo_this_version", latestVersion)
                configSettings.log(self, "Set override_kobo_this_version to "+str(latestVersion))
            elif foundMatch == False and latestVersion is not None:
                configSettings.setSetting(self, "override_kobo_this_version", latestVersion)
                configSettings.log(self, "With fear set override_kobo_this_version to "+str(latestVersion))
            else:
                configSettings.setSetting(self, "override_kobo_this_version", "0.00.00000")
                configSettings.log(self, "Found no patch-anyway option")

    def tryToFindLatestPatch(self, index):
        configSettings.log(self, "Check for matching version ...")
        foundMatch = False
        allPatchVersions = self.parsePatchJson()
        if len(allPatchVersions) == 0:
            configSettings.log(self, "Error: Could not find any patches")
            return
        choosenFirmware = configSettings.getSetting(self, "kobo_this_version")

        chosen_tuple = self.version_to_tuple(choosenFirmware)
        closest_lower_version = None
        closest_lower_tuple = None

        for version in allPatchVersions:
            current_tuple = self.version_to_tuple(version)
            
            if current_tuple == chosen_tuple:
                foundMatch = True
                break
            
            # Suche die Version direkt vor chosenFirmware
            if current_tuple < chosen_tuple:
                if closest_lower_tuple is None or current_tuple > closest_lower_tuple:
                    closest_lower_tuple = current_tuple
                    closest_lower_version = version 

        # Found possible patch version, checking if compatible 
        if not foundMatch and closest_lower_version is not None:
            choosenKoboVersionList = updateDb.getRelevantData(self, 0)
            for v in choosenKoboVersionList:
                    if v == closest_lower_version:
                        foundMatch = True
                        configSettings.log(self, f"No exact match, but previous version '{closest_lower_version}' accepted as match.")
                        break
                    else:
                        configSettings.log(self, f"{v}' is not '{closest_lower_version}' ...")
                        foundMatch = False
                        pass       
        self._view.tab_widget.labelPatchAnywayResult.show()                    
        if foundMatch:
            configSettings.log(self, f"Match found ({closest_lower_version}) for firmware: {choosenFirmware}")
            self._view.tab_widget.labelPatchAnywayResult.setText("Latest patch is for: "+closest_lower_version)
            self._view.tab_widget.labelPatchAnywayResult.setStyleSheet('font-weight:bold')
        elif foundMatch == False and closest_lower_version is not None:
            self._view.tab_widget.labelPatchAnywayResult.setText("Latest patch is for: "+closest_lower_version+", but this was never released for your Kobo!")
            self._view.tab_widget.labelPatchAnywayResult.setStyleSheet('font-weight:bold')
        elif foundMatch == False and closest_lower_version is None:
            configSettings.log(self, "No matching firmware version found.")
            self._view.tab_widget.labelPatchAnywayResult.setText("There isn't any compatible patch")
            self._view.tab_widget.labelPatchAnywayResult.setStyleSheet('color:red; font-weight:bold')
        return foundMatch, closest_lower_version

    def version_to_tuple(self, version):
        parts = re.findall(r'\d+', version)
        return tuple(int(part) for part in parts)
    
    def window_patch_anyway_help(self, index):
        dialog = QDialog()
        dialog.setWindowTitle("Patch anyway information")
        dialog.setMinimumSize(500, 400)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        text = (
            f"<html><body><h3>For recent Kobo firmwares, there are currently no up-to-date patches available.</h3>"
            "However, <b>you can activate <u>'Patch anyway'</u> to use an older patch version, which may still work most of the time.</b>.<br>"
            "KoboPatchFan will automatically use the most recent available patch version based on your firmware selection!<br><br>"
            "But some patches may not work correctly. This is especially the case for newer Kobos and versions above 4.x<br><br>"
            "Sometimes, only small values need to be adjusted. You can edit the values of all patches in KoboPatchFan "
            "by clicking \"Edit\" in tab (2).<br><br>"
            "<b>There is an active discussion about modified patches on the MobileRead forum</b>:<br>"
            "<a href='https://www.mobileread.com/forums/forumdisplay.php?f=247'>https://www.mobileread.com/forums/forumdisplay.php?f=247</a><br><br>"
            "<b>For background information on the delay, you can view the discussion on GitHub:<br>"
            "<a href='https://github.com/pgaskin/kobopatch-patches/issues/148'>https://github.com/pgaskin/kobopatch-patches/issues/148</a><br><br></body></html>"
        )
        text_edit.setHtml(text)
        layout.addWidget(text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        return dialog.exec() == QDialog.DialogCode.Accepted

    