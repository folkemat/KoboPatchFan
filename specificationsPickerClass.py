
#Filename: specificationsPickerClass.py

from configSettingsClass import configSettings
from PyQt6.QtCore import Qt

class specificationsPicker:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view

    def initComboKobos(self):
        #fill the combo with saved config data:
        koboDevice = configSettings.getSetting(self, "kobo_device")
        #set to last choose:
        index = self._view.tab_widget.combo.findText(koboDevice, Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            self._view.tab_widget.combo.setCurrentIndex(index)
            self._view.tab_widget.labelSelectedKobo.setText("<h4>Kobo "+self._view.tab_widget.combo.currentText()+"</h4>")
            self._view.tab_widget.labelSelectedKobo.setStyleSheet('color:green; font-weight:bold')
            self._view.tab_widget.label_kobo.setText("Kobo: <b>"+self._view.tab_widget.combo.currentText()+"</b>")
        else:
            self._view.tab_widget.labelSelectedKobo.setText("<h4>No Kobo selected</h4>")
            self._view.tab_widget.labelSelectedKobo.setStyleSheet('color:red; font-weight:bold')
            self._view.tab_widget.label_kobo.setText("Kobo: <b>None</b>")
                
    def confirmKobo(self):
        input = self._view.tab_widget.combo.currentText()
        configSettings.setSetting(self, "kobo_device", str(input))
        self._view.tab_widget.labelSelectedKobo.setText("<h4>Kobo "+str(input)+"</h4>")
        self._view.tab_widget.labelSelectedKobo.setStyleSheet('color:green; font-weight:bold')
        self._view.tab_widget.label_kobo.setText("Kobo: <b>"+str(input)+"</b>")

    def comboSelectKobo(self, index=None):
        pass