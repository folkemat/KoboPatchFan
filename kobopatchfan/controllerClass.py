# Filename: controllerClass.py

from PyQt6.QtCore import QObject
from functools import partial
from workingDirClass import WorkingDir
from versionPickerClass import versionPicker
from specificationsPickerClass import specificationsPicker
from updateDbClass import updateDb
from verifyClass import verifyDownload
from downloadAllClass import downloadAllClass
from editorClass import editor
from generatorClass import generator
from checkerClass import checkerClass
from savedPatchesClass import savedPatches
from configSettingsClass import configSettings

class kpController(QObject):
    """KoboPatchFan's Controller class."""
    def __init__(self, view, settings):
        """Controller initializer."""
        super(kpController, self).__init__()

        self.working_dir = WorkingDir(settings, view)
        self.version_picker = versionPicker(settings, view)
        self.specifications_picker = specificationsPicker(settings, view)
        self.update_db = updateDb(settings, view)
        self.verify_download = verifyDownload(settings, view)
        self.download_all = downloadAllClass(settings, view)
        self.editor = editor(settings, view)
        self.generator = generator(settings, view)
        self.checker = checkerClass(settings, view)
        self.savedPatches = savedPatches(settings, view)
        #for easier use
        self._view = view
        self._settings = settings
        # Connect pyqtSignals and pyqtSlots
        self._connectpyqtSignals()
        #Ini
        self.working_dir.checkForFolder()
        self.update_db.checkForDb()
        self.specifications_picker.initComboKobos()
        self.version_picker.initComboVersions()
        self._view.statusbar.showMessage("Current target firmware: "+self.checker.readKobopatchyaml()+"")
            
    def _connectpyqtSignals(self):
        """Connect pyqtSignals and pyqtSlots."""
        #Working dir stuff
        self._view.tab_widget.openFolderButton.clicked.connect(partial(self.working_dir.openWorkingFolder))
        #Specification picker stuff
        self._view.tab_widget.combo.activated.connect(partial(self.specifications_picker.comboSelectKobo))
        self._view.tab_widget.combo.currentIndexChanged.connect(self.specifications_picker.confirmKobo)
        self._view.tab_widget.combo.currentIndexChanged.connect(partial(self.version_picker.buttonUpdateVersions))
        #Version picker stuff
        #self._view.tab_widget.buttonUpdateVersions.clicked.connect(partial(self.version_picker.buttonUpdateVersions))
        self._view.tab_widget.comboVersions.activated.connect(partial(self.version_picker.comboVersions))
        self._view.tab_widget.comboVersions.currentIndexChanged.connect(partial(self.version_picker.confirmVersions))
        self._view.tab_widget.buttonPickLatest.clicked.connect(partial(self.version_picker.pick_latest_version))
        #Verify stuff
        self._view.tab_widget.comboVersions.currentIndexChanged.connect(partial(self.verify_download.verifyFirmwarePatch))
        self._view.tab_widget.combo.currentIndexChanged.connect(partial(self.verify_download.verifyFirmwarePatch))
        self._view.tab_widget.checkbox_patch_anyway.stateChanged.connect(partial(self.verify_download.tryToPatchAnyway))
        self._view.tab_widget.button_patch_anyway_help.clicked.connect(partial(self.verify_download.window_patch_anyway_help))
        #Update db stuff
        self._view.tab_widget.buttonUpdateDb.clicked.connect(partial(self.update_db.downloadDb))
        #download stuff
        self._view.tab_widget.downloadStart_button.clicked.connect(partial(self.download_all.startButton))
        self._view.tab_widget.buttonDownloadPauseResume.clicked.connect(partial(self.download_all.pause_resume))
        self._view.tab_widget.buttonDownloadCancel.clicked.connect(partial(self.download_all.stop_download))
        #editor stuff
        self._view.tab_widget.reload_button.clicked.connect(partial(self.editor.reloadFile))
        self._view.tab_widget.search_edit.textChanged.connect(partial(self.editor.filter_checkboxes))
        self._view.tab_widget.deselect_button.clicked.connect(partial(self.editor.deselect_checkboxes))
        self._view.tab_widget.open_src_button.clicked.connect(partial(self.editor.openFolderSrc))
        self._view.tab_widget.save_kobopatch_button.clicked.connect(partial(self.editor.save_kobopatch))
        self._view.tab_widget.show_selected_button.clicked.connect(partial(self.editor.show_selected_options))
        #editor tabs
        self._view.tab_widget.tab1_button.clicked.connect(lambda: self.editor.switchTab(0))
        self._view.tab_widget.tab2_button.clicked.connect(lambda: self.editor.switchTab(1))
        self._view.tab_widget.tab3_button.clicked.connect(lambda: self.editor.switchTab(2))
        self._view.tab_widget.tab4_button.clicked.connect(lambda: self.editor.switchTab(3))
        self._view.tab_widget.tabs.currentChanged.connect(partial(self.check_current_tab))
        #gen stuff
        self._view.tab_widget.run_button.clicked.connect(partial(self.generator.runScript))
        self._view.tab_widget.open_folder_button.clicked.connect(partial(self.generator.openFolderOut))
        self._view.tab_widget.export_button.clicked.connect(partial(self.generator.doTheExport))
        self._view.tab_widget.show_all_patches_gen.clicked.connect(partial(self.generator.show_info_dialog))
        #saved patches stuff
        self._view.tab_widget.kobopatch_reload_button.clicked.connect(partial(self.savedPatches.loadKobopatchFile))
        self._view.tab_widget.kobopatch_remove_all_button.clicked.connect(partial(self.savedPatches.kobopatch_remove_all))
        self._view.tab_widget.kobopatch_deactivate_all_button.clicked.connect(partial(self.savedPatches.kobopatch_deactivate_all))
        self._view.tab_widget.kobopatch_activate_all_button.clicked.connect(partial(self.savedPatches.kobopatch_activate_all))
    
    def check_current_tab(self, index):
        self._view.statusbar.showMessage("Current target firmware: "+self.checker.readKobopatchyaml())
        if index == 1:  # Tab2: Select-config
            self.editor.reloadFile()
        elif index == 3:  # Tab4: Saved patches
            self.savedPatches.loadKobopatchFile()