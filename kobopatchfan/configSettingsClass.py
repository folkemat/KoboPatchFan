# Filename: configSettingsClass.py

import os
from PyQt6.QtCore import QTime, QStandardPaths

class configSettings:
    allKoboDevices = [
        ("Touch A/B",["kobo3", "00000000-0000-0000-0000-000000000310", "Kobo Touch A/B"]),
        ("Touch C",["kobo4", "00000000-0000-0000-0000-000000000320", "Kobo Touch C"]),
        ("Mini",["kobo4", "00000000-0000-0000-0000-000000000340", "Kobo Mini"]),
        ("Glo",["kobo4", "00000000-0000-0000-0000-000000000330", "Kobo Glo"]),
        ("Glo HD",["kobo6", "00000000-0000-0000-0000-000000000371", "Kobo Glo HD"]),
        ("Touch 2.0",["kobo6", "00000000-0000-0000-0000-000000000372", "Kobo Touch 2.0"]),
        ("Aura",["kobo5", "00000000-0000-0000-0000-000000000360", "Kobo Aura"]),
        ("Aura HD",["kobo4", "00000000-0000-0000-0000-000000000350", "Kobo Aura HD"]),
        ("Aura H2O",["kobo5", "00000000-0000-0000-0000-000000000370", "Kobo Aura H2O"]),
        ("Aura H2O Edition 2 v1",["kobo6", "00000000-0000-0000-0000-000000000374", "Kobo Aura H2O Edition 2 v1"]),
        ("Aura H2O Edition 2 v2",["kobo7", "00000000-0000-0000-0000-000000000378", "Kobo Aura H2O Edition 2 v2"]),
        ("Aura ONE",["kobo6", "00000000-0000-0000-0000-000000000373", "Kobo Aura ONE"]),
        ("Aura ONE Limited Edition",["kobo6", "00000000-0000-0000-0000-000000000381", "Kobo Aura ONE Limited Edition"]),
        ("Aura Edition 2 v1",["kobo6", "00000000-0000-0000-0000-000000000375", "Kobo Aura Edition 2 v1"]),
        ("Aura Edition 2 v2",["kobo7", "00000000-0000-0000-0000-000000000379", "Kobo Aura Edition 2 v2"]),
        ("Nia",["kobo7", "00000000-0000-0000-0000-000000000382", "Kobo Nia"]),
        ("Clara HD",["kobo7", "00000000-0000-0000-0000-000000000376", "Kobo Clara HD"]),
        ("Forma",["kobo7", "00000000-0000-0000-0000-000000000380", "Kobo Forma"]),
        ("Libra H2O",["kobo7", "00000000-0000-0000-0000-000000000384", "Kobo Libra H2O"]),
        ("Elipsa",["kobo8", "00000000-0000-0000-0000-000000000387", "Kobo Elipsa"]),
        ("Sage",["kobo8", "00000000-0000-0000-0000-000000000383", "Kobo Sage"]),
        ("Libra 2",["kobo9", "00000000-0000-0000-0000-000000000388", "Kobo Libra 2"]),
        ("Clara 2E",["kobo10", "00000000-0000-0000-0000-000000000386", "Kobo Clara 2E"]),
        ("Elipsa 2E",["kobo11", "00000000-0000-0000-0000-000000000389", "Kobo Elipsa 2E"]),
        ("Libra Colour",["kobo11", "00000000-0000-0000-0000-000000000390", "Kobo Libra Colour"]),
        ("Clara BW",["kobo12", "00000000-0000-0000-0000-000000000391", "Kobo Clara BW"]),
        ("Clara Colour",["kobo12", "00000000-0000-0000-0000-000000000393", "Kobo Clara Colour"])
        ]
    documents_folder = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
    working_folder = "KoboPatchFan"
    app_folder = os.path.join(documents_folder, working_folder)

    def __init__(self, settings):
        self._settings = settings
        #settings.remove("working_dir")
        #settings.remove("working_folder")

        filename_libnickel = "libnickel.so.1.0.0.yaml"
        filename_libadobe = "libadobe.so.yaml"
        filename_librmsdk = "librmsdk.so.1.0.0.yaml"
        filename_nickel = "nickel.yaml"
        
        allStandardSettings =	{
        "kobo_device": "Forma",
        "kobo_this_version": "0.00.00000",
        "override_kobo_this_version": "0.00.00000",
        "filename_libnickel":filename_libnickel,
        "filename_libadobe":filename_libadobe,
        "filename_librmsdk":filename_librmsdk,
        "filename_nickel":filename_nickel
        }
        for standardSettingElements in allStandardSettings:
            if settings.contains(standardSettingElements) == False:
                settings.setValue(standardSettingElements, allStandardSettings[standardSettingElements])
                #print("Found NO standard setting: key={} with value={}".format(standardSettingElements, allStandardSettings[standardSettingElements]))
            else:
                #print("Found standard setting: key={} with value={}".format(standardSettingElements, allStandardSettings[standardSettingElements]))
                pass
    def getSetting(self, key):
        return self._settings.value(key)

    def doesSettingExist(self, key):
        if self._settings.contains(key):
            return True
        return False

    def setSetting(self, key, newValue):
        self._settings.setValue(key, newValue)

    def log(self, text):
        try:
            current_time = QTime.currentTime().toString("hh:mm:ss")
            self._view.tab_widget.log_text.append("[" + current_time + "]: " + text)
        except Exception as e:
            #print (e)
            pass