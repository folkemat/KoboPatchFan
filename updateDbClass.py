#Filename: updateDbClass.py

import os
import re
from configSettingsClass import configSettings
from downloadThreadClass import DownloadThread

class updateDb:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        self.updateThreadDone = True

    def downloadPatchVersions(self):
        url = "https://api.github.com/repos/pgaskin/kobopatch-patches/releases/latest"
        path = str(configSettings.getSetting(self, "working_dir"))
        filename = "patches.json"
        file_path = os.path.join(path, filename)
        configSettings.log(self, "Downloading patches.json from "+url+" to "+file_path)
        # Start the download thread with the URL and save path
        if self.updateThreadDone == True:
            self.download_thread = DownloadThread(url, file_path)
            # Connect the pyqtSignals from the download thread
            self.download_thread.finished.connect(self.downloadPatchVersionsFinish)
            self.download_thread.error.connect(self.downloadPatchVersionsError)
            self.download_thread.start()
            self.updateThreadDone = False
            self._view.tab_widget.buttonUpdateDb.setEnabled(False)
        else:
            pass

    def downloadPatchVersionsError(self, error):
        configSettings.log(self, "Error while download patch.json, aborting: "+error)
        self._view.tab_widget.buttonUpdateDb.setEnabled(True)
        self.updateThreadDone = True

    def downloadPatchVersionsFinish(self):
        self._view.tab_widget.labelUpdateDbLastTime.setText("Successfully downloaded db (2/2)")
        configSettings.log(self, "Finished downloading patches.json")
        self._view.tab_widget.buttonUpdateDb.setEnabled(True)
        self.updateThreadDone = True
        self.checkForDb()
    
    def checkForDb(self):
        status = self.fileExistence()
        if status == 0:
            self._view.tab_widget.labelUpdateDbStatus.setText("Status: No database (0/2) present, click Update!")
            return
        else:
            if status == 1:
                self._view.tab_widget.labelUpdateDbStatus.setText("Status: Database (2/2) present")
            elif status == 2:
                self._view.tab_widget.labelUpdateDbStatus.setText("Status: Missing db (1/2): patches.json is there, but kfw.js is missing")
                self._view.tab_widget.labelUpdateDbLatest.setText("Critical: Download the latest database to continue")
                self._view.tab_widget.labelUpdateDbLatest.setStyleSheet('color:red; font-weight:bold')
                return
            elif status == 3:
                self._view.tab_widget.labelUpdateDbStatus.setText("Status: Missing db (1/2): kfw.js is there, but patches.json is missing")
                self._view.tab_widget.labelUpdateDbLatest.setText("Critical: Download the latest database to continue")
                self._view.tab_widget.labelUpdateDbLatest.setStyleSheet('color:red; font-weight:bold')
                return
        latestDate = self.getRelevantData(1)
        self._view.tab_widget.labelUpdateDbLatest.setText("Latest firmware from: "+str(latestDate))
        self._view.tab_widget.labelUpdateDbLatest.setStyleSheet('color:green; font-weight:bold')
        #fill the combo firmware box
        versionList = self.getRelevantData(0)
        if versionList:
            self._view.tab_widget.comboVersions.clear()
            self._view.tab_widget.comboVersions.addItems(versionList)

    #download the kfw.db and connect to parse the content
    def downloadDb(self):
        #first: Download the database
        url = "https://pgaskin.net/KoboStuff/kfw.db.js"
        path = str(configSettings.getSetting(self, "working_dir"))
        filename = "kfw.js"
        file_path = os.path.join(path, filename)
        configSettings.log(self, "Downloading kfw.js from "+url+" to "+file_path)
        # Start the download thread with the URL and save path
        if self.updateThreadDone == True:
            self.download_thread = DownloadThread(url, file_path)
            # Connect the pyqtSignals from the download thread
            self.download_thread.finished.connect(self.downloadFinished)
            self.download_thread.error.connect(self.downloadError)
            self.download_thread.start()
            self._view.tab_widget.buttonUpdateDb.setEnabled(False)
            self.updateThreadDone = False
    
    def downloadError(self, error):
        self._view.tab_widget.labelUpdateDbLastTime.setText("Status: Error: "+error)
        configSettings.log(self, "Download Error: "+error)
        self._view.tab_widget.buttonUpdateDb.setEnabled(True)
        self.updateThreadDone = True

    def downloadFinished(self):
        self._view.tab_widget.labelUpdateDbLastTime.setText("Successfully downloaded db (1/2)")
        self.updateThreadDone = True
        self._view.tab_widget.buttonUpdateDb.setEnabled(True)
        self.downloadPatchVersions() #after that,  self.checkForDb()


    def getRelevantData(self, mode):
        path = str(configSettings.getSetting(self, "working_dir"))
        filename = "kfw.js"
        file_path = os.path.join(path, filename)

        #Open file with the target Javascript array db
        try:
            with open(file_path, "r") as f:
                content = f.read()
        except Exception as e:
            configSettings.log(self, "Error getRelevantData 0: "+str(e))
            return

        #Search for Array-Literal
        match = re.search("return \[(.*)\],\n]", content, re.DOTALL)
        if not match:
            configSettings.log(self, "Error getRelevantData: Array literal not found")
            return
        try:     
            #Extract the array as a string
            array_str = match.group(1)

            #Extract each element of the array as a list
            elements = re.findall("\[(.*?)\]", array_str)

            #Convert each element as a list of strings
            data = [element.strip().split(",") for element in elements]

            #Convert each element to a list of strings
            data = [tuple(map(lambda x: x.strip().strip('"'), element)) for element in data] #data = [['a', 'b', 'c'], ['d', 'e', 'f']]   
        except Exception as e:
            configSettings.log(self, "Error getRelevantData 1: An unexpected error occurred: "+str(e))
            return
             
        if(mode == 1): #only the last entry
            return data[-1][3]
        if (mode == 2):
            return data

        #handle the data
        if configSettings.doesSettingExist(self, "kobo_device"):
            koboDevice = configSettings.getSetting(self, "kobo_device")
        allKobos = configSettings(self._settings).allKoboDevices
        
        koboVersion = "0"
        try:
            for element in allKobos:
                if koboDevice in element:
                    koboVersion = str(element[1][1])
                    break
            koboVersion = koboVersion.replace("00000000-0000-0000-0000-000000000", "")
            versionList = []
            for sublist in data:
                for element in sublist:
                    if koboVersion in element:
                        versionList.append(sublist[2])
                        break
        except Exception as e:
            configSettings.log(self, "Error getRelevantData 2: An unexpected error occurred: "+str(e))
            return
        return versionList

    def fileExistence(self):
        path = str(configSettings.getSetting(self, "working_dir"))
        kfwFilename = "kfw.js"
        kfw_file_path = os.path.join(path, kfwFilename)
        patchesFilename = "patches.json"
        patches_file_path = os.path.join(path, patchesFilename)
        kfwThere = False
        patchesThere = False
        try:
            if os.path.isfile(kfw_file_path):
                kfwThere = True
            else:
                kfwThere = False

            if os.path.isfile(patches_file_path):
                patchesThere = True
            else:
                patchesThere = False
            if kfwThere and patchesThere:
                return 1
            if not kfwThere and patchesThere:
                return 2
            if kfwThere and not patchesThere:
                return 3
            if not kfwThere and not patchesThere:
                return 0
        except:
            return 0