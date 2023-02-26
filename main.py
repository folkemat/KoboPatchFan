# Filename: main.py

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QIcon
from mainWindowStuff import KoboPatchFanUi
from controllerClass import kpController
from configSettingsClass import configSettings
from workingDirClass import WorkingDir
from versionPickerClass import versionPicker
from specificationsPickerClass import specificationsPicker
from updateDbClass import updateDb
from verifyClass import verifyDownload
from downloadAllClass import downloadAllClass
from editorClass import editor
from generatorClass import generator
from checkerClass import checkerClass

# load from mainWindowStoff.py the GUI
class kpMainWindowIni(KoboPatchFanUi):
    def __init__(self):
        super().__init__()

def main():
    """Main function."""
    # Create an instance of QApplication
    kobopatchfan = QApplication(sys.argv)
    kobopatchfan.setWindowIcon(QIcon('kpf.ico'))
    # Show the GUI
    view = kpMainWindowIni()
    view.show()
    # Create instances of the model and the controller
    settings = QSettings('KoboPatchFanCompany', 'KoboPatchFan')
    # settings.clear()
    configSettings(settings=settings)
    kpController(view=view, settings=settings)
    WorkingDir(view=view, settings=settings)
    versionPicker(view=view, settings=settings)
    specificationsPicker(view=view, settings=settings)
    updateDb(view=view, settings=settings)
    verifyDownload(view=view, settings=settings)
    downloadAllClass(view=view, settings=settings)
    editor(view=view, settings=settings)
    generator(view=view, settings=settings)
    checkerClass(view=view, settings=settings)

    # Execute the main loop
    sys.exit(kobopatchfan.exec())

if __name__ == '__main__':
    main()