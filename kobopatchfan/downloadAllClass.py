#Filename: downloadAllClass.py

import os
import re
import json
import shutil
from configSettingsClass import configSettings
from downloadThreadClass import DownloadThread
from extractThreadClass import ExtractThread
from updateDbClass import updateDb
from checkerClass import checkerClass
from PyQt6.QtWidgets import QLabel, QMessageBox

class downloadAllClass:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        self.patchLink = "Unknown"
        self.firmwareFileName = "Unknown"
        self.patchFileName = "Unknown"
        self.checker = checkerClass(settings, view)

    def security_question(self):
        firmwareVersion = configSettings.getSetting(self, "kobo_this_version")
        koboDevice = configSettings.getSetting(self, "kobo_device")
        result = QMessageBox.question(None, "Confirm configuration", "Kobo: "+koboDevice+"\nFirmware: "+firmwareVersion+"\n\nIs the above configuration correct?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        if result == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    def startButton(self):
        if not self.security_question():
            return
        dbConfigs = self.readDbConfig()
        if dbConfigs:
            targetUrls = self.createDownloadLink(dbConfigs)
        else: 
            configSettings.log(self, "Error: Could not read configs for download")
            self._view.tab_widget.labelDownloadInfo.setText("Error: Could not read configs for download")
            return
        if targetUrls:
            self.startDownloading(targetUrls)
        else:
            configSettings.log(self, "Error: Could not create all download links")
            self._view.tab_widget.labelDownloadInfo.setText("Error: Could not create all download links")
            return
    
    def startDownloading(self, urls):
        firmwareLink = urls[0]
        self.patchLink = urls[1]
        path = str(configSettings(self._settings).app_folder)
        #start with the download of the FIRMWARE
        self.download_firmware_thread = DownloadThread(firmwareLink, path)
        self.download_firmware_thread.finished.connect(self.firmware_download_finished) #start patch-download after finish
        self.download_firmware_thread.error.connect(self.error)
        self.download_firmware_thread.progress.connect(self.update_progress)
        self.download_firmware_thread.speed.connect(self.update_speed)
        self.download_firmware_thread.remaining_time.connect(self.update_remaining_time)
        self.download_firmware_thread.size.connect(self.size)
        self.download_firmware_thread.start()
        self._view.tab_widget.downloadStart_button.setEnabled(False)
        self._view.tab_widget.downloadStart_button.setText("Downloading (1/2)...")
        self._view.tab_widget.buttonDownloadCancel.setEnabled(True)
        self._view.tab_widget.buttonDownloadPauseResume.setEnabled(True)
        self._view.tab_widget.labelDownloadInfo.setText("Downloading firmware files (1/2) ...")
    
    def firmware_download_finished(self, filename):
        self.firmwareFileName = filename #safe the name for later
        configSettings.log(self, "Download firmware finished")
        self._view.tab_widget.downloadStart_button.setEnabled(True)
        self._view.tab_widget.buttonDownloadCancel.setEnabled(False)
        self._view.tab_widget.buttonDownloadPauseResume.setEnabled(False)
        self._view.tab_widget.downloadStart_button.setText("Start")
        self._view.tab_widget.labelDownloadInfo.setText("Firmware downloaded successfully")

        #after firmware is finish, begin patch download
        configSettings.log(self, "Starting patch download ...")
        path = str(configSettings(self._settings).app_folder)
        self.download_patch_thread = DownloadThread(self.patchLink, path)
        self.download_patch_thread.finished.connect(self.patch_download_finished)
        self.download_patch_thread.error.connect(self.error)
        self.download_patch_thread.progress.connect(self.update_progress)
        self.download_patch_thread.speed.connect(self.update_speed)
        self.download_patch_thread.remaining_time.connect(self.update_remaining_time)
        self.download_patch_thread.size.connect(self.size)
        self.download_patch_thread.start()
        self._view.tab_widget.downloadStart_button.setEnabled(False)
        self._view.tab_widget.downloadStart_button.setText("Downloading (2/2) ...")
        self._view.tab_widget.buttonDownloadCancel.setEnabled(True)
        self._view.tab_widget.buttonDownloadPauseResume.setEnabled(True)
        self._view.tab_widget.labelDownloadInfo.setText("Downloading patch files (2/2)...")

    def patch_download_finished(self, filename):
        configSettings.log(self, "Download patch finished")
        self._view.tab_widget.downloadStart_button.setEnabled(True)
        self._view.tab_widget.buttonDownloadCancel.setEnabled(False)
        self._view.tab_widget.buttonDownloadPauseResume.setEnabled(False)
        self._view.tab_widget.downloadStart_button.setText("Start")
        self._view.tab_widget.labelDownloadInfo.setText("(2/2) Patch & firmware downloaded successfully!")
        #after download is finish, start the extraction of the PATCH
        if self._view.tab_widget.checkBoxExtract.isChecked() == True:
            self.startExtracting(filename)
        else:
            self._view.tab_widget.labelDownloadInfo.setText("Download (2/2) successful - extraction not requested.")
    
    def startExtracting(self, filename):
        #start with the extraction of the PATCH
        configSettings.log(self, "Start extraction of patch "+filename+" ...")
        path = str(configSettings(self._settings).app_folder)
        patch_file_path = os.path.join(path, filename)
        self.extract_thread = ExtractThread(patch_file_path, path)
        self.extract_thread.extractionFinished.connect(self.patch_extraction_finished)
        self.extract_thread.extractionError.connect(self.error)
        self.extract_thread.progressUpdated.connect(self.update_progress)
        self.extract_thread.extractionSpeed.connect(self.update_speed)
        self.extract_thread.extractionRemainingTime.connect(self.update_remaining_time)
        self.extract_thread.extractionSize.connect(self.size)
        self.extract_thread.start()
        self._view.tab_widget.downloadStart_button.setEnabled(False)
        self._view.tab_widget.downloadStart_button.setText("Extracting ...")
        self._view.tab_widget.labelDownloadInfo.setText("Extracting patch files ...")
    
    def patch_extraction_finished(self):
        configSettings.log(self, "Extraction patch finished")
        self._view.tab_widget.downloadStart_button.setEnabled(True)
        self._view.tab_widget.downloadStart_button.setText("Start")
        self._view.tab_widget.labelDownloadInfo.setText("(1/2) Extracted patch successfully")
        #after download is finish, COPY the FIRMWARE.zip to ./src
        self.copyFirmware()
    
    def copyFirmware(self):
        try:
            path = str(configSettings(self._settings).app_folder)
            src_file_path = os.path.join(path, self.firmwareFileName)
            destination_folder = os.path.join(path, "src")
            dst_dir_path = os.path.join(path, destination_folder)
            configSettings.log(self, "Start copying firmware file "+self.firmwareFileName+" to "+dst_dir_path)
            shutil.copy2(src_file_path, dst_dir_path)
            self._view.tab_widget.labelDownloadInfo.setText("Done! Download, extraction, copying was successful.")
            self._view.statusbar.showMessage("New target firmware: "+self.checker.readKobopatchyaml())
            configSettings.log(self, "Successfully copied firmware file "+self.firmwareFileName)
        except FileNotFoundError as e:
            self._view.tab_widget.labelDownloadInfo.setText("Error: File "+self.firmwareFileName+" not found.")
            configSettings.log(self, "Error: File "+self.firmwareFileName+" not found.")
        except shutil.Error as e:
            self._view.tab_widget.labelDownloadInfo.setText("Error: Unable to copy "+self.firmwareFileName+".")
            configSettings.log(self, "Error: Unable to copy "+self.firmwareFileName+".")
        except Exception as e:
            self._view.tab_widget.labelDownloadInfo.setText("Error: An unexpected error occurred while copying "+self.firmwareFileName+".")
            configSettings.log(self, "Error: An unexpected error occurred while copying "+self.firmwareFileName+".")
        
    def firmware_extraction_finished(self):
        configSettings.log(self, "Extraction firmware finished")
        self._view.tab_widget.downloadStart_button.setEnabled(True)
        self._view.tab_widget.downloadStart_button.setText("Start")
        self._view.tab_widget.labelDownloadInfo.setText("(2/2) Extracted patch and firmware files successfully!")

    def update_progress(self, progress):
        # Update the progress bar with the new progress
        self._view.tab_widget.progress_bar.setValue(progress)

    def update_speed(self, speed):
        self._view.tab_widget.label_speed.setText("Speed: "+str(speed))

    def update_remaining_time(self, remaining_time):
        self._view.tab_widget.label_remaining.setText("Remaining time: "+remaining_time)

    def size(self, size):
        self._view.tab_widget.label_size.setText("Size: "+size)

    def error(self, error):
        configSettings.log(self, "Error: "+error)
        self._view.tab_widget.downloadStart_button.setEnabled(True)
        self._view.tab_widget.buttonDownloadCancel.setEnabled(False)
        self._view.tab_widget.buttonDownloadPauseResume.setEnabled(False)
        self._view.tab_widget.downloadStart_button.setText("Start")
        self._view.tab_widget.labelDownloadInfo.setText("An error occurred. Check the log.")
        return

    def createDownloadLink(self, dbConfig):
        dh = dbConfig[0]
        dk = dbConfig[1]
        da = dbConfig[2]
        patchLinkList = dbConfig[3]
        firmwareLink = "Unknown"
        patchLink = "Unknown"
        data = updateDb.getRelevantData(self, 2)
        
        allKobos = configSettings(self._settings).allKoboDevices
        firmwareVersion = configSettings.getSetting(self, "kobo_this_version")
        koboDevice = configSettings.getSetting(self, "kobo_device")
        koboVersion = "0"
        try:
            for element in allKobos:
                if koboDevice in element:
                    configSettings.log(self, "Code for "+koboDevice+" is "+element[1][1])
                    koboVersion = element[1][1]
                    break
            koboVersion = koboVersion.replace("00000000-0000-0000-0000-000000000", "")
            for sublist in data:
                for element in sublist:
                    if koboVersion in element:
                            if firmwareVersion in sublist[4]:
                                firmwareLink = sublist[4]
                                break
        except Exception as e:
            configSettings.log(self, "Error: Could not perform createDownloadLink: "+str(e))
            return
        if  firmwareLink == "Unknown":
            configSettings.log(self, "Error: Could not find firmware url for "+koboDevice+" with firmware "+firmwareVersion)
            return
        if "dk+" in firmwareLink:
            firmwareLink = firmwareLink.replace('dk+"', dk+""+dh)
        elif "da+" in firmwareLink:
            firmwareLink = firmwareLink.replace('da+"', da+""+dh)
        else:
            configSettings.log(self, "Error: Could not really read firmware link, dk and da missing")
            return
        configSettings.log(self, "Firmware URL: "+firmwareLink)

        try:
            #create the patch download-link
            for link in patchLinkList:
                if firmwareVersion in link:
                    patchLink = link
                    configSettings.log(self, "Found patch URL: "+patchLink)
                    break

            if  patchLink == "Unknown":
                configSettings.log(self, "Error: Could NOT find patch URL for "+koboDevice+" with firmware "+firmwareVersion)
                return
        except Exception as e:
            configSettings.log(self, "Error createDownloadLink: "+str(e))
            return
        return firmwareLink, patchLink

    def readDbConfig(self):
        path = str(configSettings(self._settings).app_folder)
        filename = os.path.join(path, "kfw.js")
        
        if not os.path.isfile(filename):
            configSettings.log(self, "readDbConfig: File does not exist.")
            return
        try:
            with open(filename, "r") as file:
                source = file.read()
        except:
            configSettings.log("readDbConfig: Cannot read file.")
            return

        dh_pattern = r'var\s+dh\s*=\s*"([^"]+)"'
        dk_pattern = r'var\s+dk\s*=\s*"([^"]+)"'
        da_pattern = r'var\s+da\s*=\s*"([^"]+)"'
        dh_match = re.search(dh_pattern, source)
        if dh_match:
            dh = dh_match.group(1)
        else:
            configSettings.log(self, "readDbConfig: Error: could not find value for variable 'dh'")
            return

        dk_match = re.search(dk_pattern, source)
        if dk_match:
            dk = dk_match.group(1)
        else:
            configSettings.log(self, "readDbConfig: Error: could not find value for variable 'dk'")
            return

        da_match = re.search(da_pattern, source)
        if da_match:
            da = da_match.group(1)
        else:
            configSettings.log(self, "readDbConfig: Error: could not find value for variable 'da'")
            return
        configSettings.log(self, "Successfully executed readDbConfig and assigned variables")

        patchPath = str(configSettings(self._settings).app_folder)
        patchFilename = "patches.json"
        patch_file_path = os.path.join(patchPath, patchFilename)
        linkList = []
        try:
            with open(patch_file_path, 'r') as file:
                file_content = file.read()
                json_object = json.loads(file_content)
            for elements in json_object["assets"]:
                thisLink = elements["browser_download_url"]
                linkList.append(thisLink)
            configSettings.log(self, "Successfully parsed patches.json for creating download link")
        except Exception as e:
            configSettings.log(self, "Error parsing patches.json for creating download link: "+str(e))
        return dh, dk, da, linkList

    def pause_resume(self):
        if self.download_firmware_thread.pause_flag:
            self.download_firmware_thread.pause_flag = False
            self._view.tab_widget.buttonDownloadPauseResume.setText("Pause")
            self._view.tab_widget.buttonDownloadCancel.setEnabled(True)
        else:
            self.download_firmware_thread.pause_flag = True
            self._view.tab_widget.buttonDownloadPauseResume.setText("Resume")
            self._view.tab_widget.buttonDownloadCancel.setEnabled(False)

    def stop_download(self):
        self.download_firmware_thread.stop()