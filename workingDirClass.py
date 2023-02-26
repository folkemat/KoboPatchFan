
#Filename: workingDirClass.py

import sys
import subprocess
import os
import pathlib
from os.path import expanduser
from configSettingsClass import configSettings
from PyQt6.QtWidgets import QFileDialog
from validChecks import is_path_exists_or_creatable_portable

class WorkingDir:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        self.working_dir_save = 1

    def _changeWorkingDir(self):
        try:
            currentDir = pathlib.Path(configSettings.getSetting(self, "working_dir"))
            pathname = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser(str(currentDir)))
            if is_path_exists_or_creatable_portable(str(pathname)) == True: #Good path
                workingPathname = pathlib.Path(str(pathname))
                #create folder here
                if self._createFolderKoboPatchFan(workingPathname) == False:
                    configSettings.log(self, "Error: Invlid path [2]")
                    self.working_dir_save = 1
                else:
                    configSettings.log(self, "Successfully changed folder")
                    self.working_dir_save = -1
                #update label with newPath+folder
                self.updateWorkingDirLabel()
                return
            else: #Bad path
                configSettings.log(self, "Error: Bad path: Invalid dir choosen")
                return
        except Exception as e:
            configSettings.log(self, "Error: Cannot change working dir folder")
    
    def _saveWorkingDir(self, theNewPathName):
        currentDir = pathlib.Path(theNewPathName)#.as_posix()
        if currentDir.exists() == True: #good path
            self.working_dir_save = -1
            configSettings.log(self, "Good path")
        else: #bad path, show error
            self.working_dir_save  = 1
            configSettings.log(self, "Error: Bad path")

    def _createFolderKoboPatchFan(self, theNewPathName):
        folderPath = pathlib.Path(theNewPathName)
        ourFolderName = configSettings.getSetting(self, "working_folder")
        #check if path is empty
        if is_path_exists_or_creatable_portable(str(folderPath)) == False:
            #no folder? create standard one again
            standardFolderPath = pathlib.Path.cwd()
            #try again
            configSettings.log(self, "Error creating KoboPatchFan folder: Reset and try again")
            self._createFolderKoboPatchFan(standardFolderPath)
            return False
        #check for double dirs
        if str(ourFolderName) in str(folderPath):
            configSettings.log(self, "Note: Already in KoboPatchFan folder")
            return True
        try:
            p = pathlib.Path(folderPath, ourFolderName)
            p.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            configSettings.log(self, "Error: Can not create folder here: "+str(e))
            return False
        else:
            newWorkingDir = pathlib.Path(str(folderPath), str(ourFolderName))
            if is_path_exists_or_creatable_portable(str(newWorkingDir)) == True: #good path
                newWorkingDir = pathlib.Path(newWorkingDir)
                configSettings.setSetting(self, "working_dir", str(newWorkingDir))
                configSettings.log(self, "Folder KoboPatchFan successfully created")
                self.updateWorkingDirLabel()
                return True
            else: #bad path
                configSettings.log(self, "Error creating KoboPatchFan folder, bad path")
            return False    

    def showWorkingDirEdit(self):
        if self._view.tab_widget.doneWorkingDirButton.text() == "Edit":
            #self._view.tab_widget.firstStepLabel.show()
            self._view.tab_widget.changeWorkingDirButton.show()
            self._view.tab_widget.createFolderRadiobutton.show()
            self._view.tab_widget.doneWorkingDirButton.setText("Done")
        elif self._view.tab_widget.doneWorkingDirButton.text() == "Done":
            #self._view.tab_widget.firstStepLabel.hide()
            self._view.tab_widget.changeWorkingDirButton.hide()
            self._view.tab_widget.createFolderRadiobutton.hide()
            self._view.tab_widget.doneWorkingDirButton.setText("Edit")

    def updateWorkingDirRegion(self):
        if self.working_dir_save == -1: #save-mode
            self._view.tab_widget.workingDirLabel.setEnabled(False)
            #self._view.tab_widget.firstStepLabel.setText("<h3>Working directory: Save</h3>")
            self._view.tab_widget.workingDirLabel.setStyleSheet("font-weight: bold; color: black;")
            #self._view.tab_widget.firstStepLabel.setStyleSheet('background-color: lightgreen;border: 2px solid gray;')
            self._view.tab_widget.applyWorkingDirButton.setText('Edit')
            self._view.tab_widget.applyWorkingDirButton.hide()
        else: #edit-mode
            self._view.tab_widget.workingDirLabel.setEnabled(True) 
            #self._view.tab_widget.firstStepLabel.setText("<h3>Working directory: Fallback</h3>")
            self._view.tab_widget.workingDirLabel.setStyleSheet("font-weight: bold; color: green;")
            #self._view.tab_widget.firstStepLabel.setStyleSheet('color:white;background-color: darkred;border: 2px solid gray;')
            self._view.tab_widget.applyWorkingDirButton.setText('Save')
            self._view.tab_widget.applyWorkingDirButton.hide()
            
    def updateWorkingDirLabel(self):
        folderName = str(configSettings.getSetting(self, "working_dir"))
        self._view.tab_widget.workingDirLabel.setText(folderName)
        self._createFolderKoboPatchFan(folderName)
        self.updateWorkingDirRegion()
    
    def openWorkingFolder(self):
        try:
            path = str(configSettings.getSetting(self, "working_dir"))
            if sys.platform == "win32":
                os.startfile(path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, path])
        except Exception as e:
            configSettings.log(self, "Error: Could not open working dir folder")
