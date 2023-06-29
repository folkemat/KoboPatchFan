from configSettingsClass import configSettings
from PyQt6.QtCore import Qt
from updateDbClass import updateDb

class versionPicker:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
    
    def pick_latest_version(self):
        last_index = self._view.tab_widget.comboVersions.count() - 1
        last_item = self._view.tab_widget.comboVersions.itemText(last_index)
        self._view.tab_widget.comboVersions.setCurrentIndex(last_index)
        configSettings.setSetting(self, "kobo_this_version", last_item)

    def initComboVersions(self):
            koboFirmware = configSettings.getSetting(self, "kobo_this_version")
            index = self._view.tab_widget.comboVersions.findText(koboFirmware, Qt.MatchFlag.MatchFixedString)
            if index >= 0:
                self._view.tab_widget.comboVersions.setCurrentIndex(index)
                self._view.tab_widget.labelVersionSelected.setText("<h4>"+self._view.tab_widget.comboVersions.currentText()+"</h4>")
                self._view.tab_widget.labelVersionSelected.setStyleSheet('color:green; font-weight:bold')
                self._view.tab_widget.label_firmware.setText("Firmware: <b>"+self._view.tab_widget.comboVersions.currentText()+"</b>")
            else:
                self._view.tab_widget.labelVersionSelected.setText("<h4>No version selected</h4>")
                self._view.tab_widget.labelVersionSelected.setStyleSheet('color:red; font-weight:bold')
                self._view.tab_widget.label_firmware.setText("Firmware: <b>None</b>")

    def confirmVersions(self, index=None):
        input = self._view.tab_widget.comboVersions.currentText()
        if input == "":
            self._view.tab_widget.labelVersionSelected.setText("<h4>No version selected</h4>")
            self._view.tab_widget.labelVersionSelected.setStyleSheet('color:red; font-weight:bold')
            self._view.tab_widget.label_firmware.setText("Firmware: <b>None</b>")
        else:
            configSettings.setSetting(self, "kobo_this_version", input)
            self._view.tab_widget.labelVersionSelected.setText("<h4>"+input+"</h4>")
            self._view.tab_widget.labelVersionSelected.setStyleSheet('color:green; font-weight:bold')
            self._view.tab_widget.label_firmware.setText("Firmware: <b>"+input+"</b>")

    def comboVersions(self, index):
        input = self._view.tab_widget.comboVersions.currentText()
        if input == configSettings.getSetting(self, "kobo_this_version"):
            self._view.tab_widget.labelVersionSelected.setText("<h4>"+input+"</h4>")
            self._view.tab_widget.labelVersionSelected.setStyleSheet('color:green; font-weight:bold')
            self._view.tab_widget.label_firmware.setText("Firmware: <b>"+input+"</b>")
        else:
            self._view.tab_widget.labelVersionSelected.setText("<h4>"+input+"</h4>")
            self._view.tab_widget.labelVersionSelected.setStyleSheet('color:red; font-weight:bold')
            self._view.tab_widget.label_firmware.setText("Firmware: <b>None</b>")

    def buttonUpdateVersions(self, index=None):
        versionList = updateDb.getRelevantData(self, 0)
        if versionList:
            self._view.tab_widget.comboVersions.clear()
            self._view.tab_widget.comboVersions.addItems(versionList)