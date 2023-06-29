#Filename: editorClass.py

import os
from configSettingsClass import configSettings
from loadDataThreadClass import LoadDataThread
from PyQt6.QtCore import QDir, QFileInfo
from PyQt6.QtWidgets import QLabel, QMessageBox, QListWidgetItem, QGroupBox, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout
from PyQt6.QtGui import QFont
from functools import partial
import shutil
import yaml

class savedPatches:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        
        self.editor_text = ""
        self.kobopatch_checkboxes = []

    def removeAllSavedPatches(self):
        self._view.tab_widget.listWidget.clear()
        self.kobopatch_checkboxes = []
        #self._view.tab_widget.search_edit.setText("")
    
    def checkFileFolder(self, save_folder_name, save_folder):
        app_folder = str(configSettings(self._settings).app_folder)

        if not os.path.exists(save_folder):
            try:
                QDir(app_folder).mkdir(save_folder_name)
            except Exception as e:
                configSettings.log(self, "Error: Could not create kobopatch_save folder: "+str(e))
                self._view.tab_widget.savedpatches_info_label.setText("Error: Could not find and create kobopatch_save folder")
                return False

        abs_path = QDir(app_folder).filePath(save_folder_name)
        self._view.tab_widget.savedpatches_info_label.setText(str(abs_path))
        return True
    
    def checkForFile(self, kobopatch_save_file_path, kobopatch_unsave_file_path):
        
        #check if file exist, otherwise copy it to save location

        if os.path.isfile(kobopatch_save_file_path):
            return True
        elif not os.path.isfile(kobopatch_save_file_path):
            #we copy kobopatch.yaml from unsave app fir location to save location
            try:
                shutil.copy2(kobopatch_unsave_file_path, kobopatch_save_file_path)
                return True
            except Exception as e:
                configSettings.log(self, "Error: Could not copy kobopatch.yaml: "+str(e))
                self._view.tab_widget.savedpatches_info_label.setText("Error: Could not find/copy kobopatch.yaml")
                return False
    
    def checkKobopatchyamlFolderAndFile(self):
        app_folder = str(configSettings(self._settings).app_folder)
        save_folder_name = "kobopatch_save"
        save_folder = os.path.join(app_folder, save_folder_name)
        kobopatch_file_name = "kobopatch.yaml"
        kobopatch_unsave_file_path = os.path.join(app_folder, kobopatch_file_name)
        kobopatch_save_file_path = os.path.join(save_folder, kobopatch_file_name)

        if not os.path.exists(save_folder):
            try:
                QDir(app_folder).mkdir(save_folder_name)
            except Exception as e:
                configSettings.log(self, "Error: Could not create kobopatch_save folder: "+str(e))
                self._view.tab_widget.savedpatches_info_label.setText("Error: Could not find and create kobopatch_save folder")
                return False
        
        if os.path.isfile(kobopatch_save_file_path):
            return True
        elif not os.path.isfile(kobopatch_save_file_path):
            #we copy kobopatch.yaml from unsave app fir location to save location
            try:
                shutil.copy2(kobopatch_unsave_file_path, kobopatch_save_file_path)
                return True
            except Exception as e:
                configSettings.log(self, "Error: Could not copy kobopatch.yaml: "+str(e))
                self._view.tab_widget.savedpatches_info_label.setText("Error: Could not find/copy kobopatch.yaml")
                return False
            
        return True

    def loadKobopatchFile(self):
        self.removeAllSavedPatches() #clean layout
        app_folder = str(configSettings(self._settings).app_folder)
        save_folder_name = "kobopatch_save"
        save_folder = os.path.join(app_folder, save_folder_name)
        kobopatch_file_name = "kobopatch.yaml"
        kobopatch_unsave_file_path = os.path.join(app_folder, kobopatch_file_name)
        kobopatch_save_file_path = os.path.join(save_folder, kobopatch_file_name)
        
        if not self.checkKobopatchyamlFolderAndFile():
            self._view.tab_widget.savedpatches_info_label.setText("Error: Could not write/read kobopatch_save folder")
            return
        
        #Processing the kobopatch.yaml file
        try:
            #Create a thread in which the data for the widgets is calculated 
            self.kobopatch_ThreadDone = False

            self.kobopatch_save_thread = LoadDataThread(kobopatch_save_file_path, 1)
            self.kobopatch_save_thread.patches_in_kobopatchyaml.connect(self.create_kobopatchsave_gui) 
            self.kobopatch_save_thread.finish_patches_in_kobopatchyaml.connect(self.finish_loaded_kobopatchyaml) 
            self.kobopatch_save_thread.start()

        except Exception as e:
            self._view.tab_widget.savedpatches_info_label.setText("Error: "+str(e))
            configSettings.log(self, "Error kobopatch.yaml: "+str(e))
            return
    
    def create_kobopatchsave_gui(self, file_name, option, state):
        option_layout = QVBoxLayout()

        kobopatch_checkbox = QCheckBox(option)
        kobopatch_checkbox.setChecked(state)
        kobopatch_checkbox.stateChanged.connect(partial(self.kobopatch_checkbox_state_changed, file_name, option, kobopatch_checkbox)) #connect all checkboxes
        self.kobopatch_checkboxes.append([kobopatch_checkbox, file_name, option])

        #fancy new font
        current_font = kobopatch_checkbox.font()
        current_size = current_font.pointSize()
        new_font = QFont(current_font.family(), current_size + 1, QFont.Weight.Bold)
        kobopatch_checkbox.setFont(new_font)

        option_name_label = QLabel("From: " + file_name)
        option_layout.addWidget(kobopatch_checkbox)
        option_layout.addWidget(option_name_label)

        self.delete_option_button = QPushButton("Remove")
        self.delete_option_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.delete_option_button)
        option_layout.addLayout(button_layout)
        self.delete_option_button.clicked.connect(partial(self.deleteOption, file_name, option))

        option_groupbox_layout = QVBoxLayout()
        option_groupbox_layout.addLayout(option_layout)
        option_groupbox = QGroupBox()
        option_groupbox.setLayout(option_groupbox_layout)
        option_groupbox.setStyleSheet("QGroupBox {border: 1px solid gray; border-radius: 5px;}")
        option_groupbox.setStyleSheet("""
        QGroupBox {
            background-color: #f0f0f0;
            border: 1px solid #b7b7b7;
            border-radius: 5px;
        }
        """)

        item = QListWidgetItem()
        item.setSizeHint(option_groupbox.sizeHint())
        self._view.tab_widget.listWidget.addItem(item)
        self._view.tab_widget.listWidget.setItemWidget(item, option_groupbox)

    def finish_loaded_kobopatchyaml(self, number_of_options, file_path):
        self._view.tab_widget.savedpatches_info_label.setText("Backed-up patches: "+str(number_of_options)+" | Location:")

        file_info = QFileInfo(file_path)
        absolute_path = file_info.absoluteFilePath()
        self._view.tab_widget.kobopatch_save_location.setText(absolute_path)
    
    def deleteOption(self, target_file_name, target_option):
        app_folder = str(configSettings(self._settings).app_folder)
        save_folder_name = "kobopatch_save"
        save_folder = os.path.join(app_folder, save_folder_name)
        kobopatch_file_name = "kobopatch.yaml"
        kobopatch_save_file_path = os.path.join(save_folder, kobopatch_file_name)
        kobopatch_unsave_file_path = os.path.join(app_folder, kobopatch_file_name)

        try: 
            with open(kobopatch_save_file_path, encoding='utf-8') as f:
                data_save = yaml.safe_load(f)
            with open(kobopatch_unsave_file_path, encoding='utf-8') as stream:
                data_unsave = yaml.safe_load(stream)

            overrides_unsave = data_unsave.get('overrides')
            overrides_save = data_save.get('overrides')

            #delete from save
            for file_name_save in overrides_save:
                if target_file_name in file_name_save:
                    options_save = overrides_save.get(file_name_save)
                    if options_save:
                        for option_save in options_save:
                            if target_option in option_save:         
                                del options_save[option_save]
                                break
            #delete from unsave
            for file_name_unsave in overrides_unsave:
                if target_file_name in file_name_unsave:
                    options_unsave = overrides_unsave.get(file_name_unsave)
                    if options_unsave:
                        for option_unsave in options_unsave:
                            if target_option in option_unsave:         
                                del options_unsave[option_unsave]
                                break

            with open(kobopatch_save_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data_save, f)
            with open(kobopatch_unsave_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data_unsave, f)
            
            self.loadKobopatchFile()
        except Exception as e:
            configSettings.log(self, "Error kobopatch.yaml: "+str(e))
            self._view.tab_widget.savedpatches_info_label.setText("Error: "+str(e))

    def kobopatch_checkbox_state_changed(self, target_file_name, target_option, kobopatch_checkbox, index=None):
        app_folder = str(configSettings(self._settings).app_folder)
        save_folder_name = "kobopatch_save"
        save_folder = os.path.join(app_folder, save_folder_name)
        kobopatch_file_name = "kobopatch.yaml"
        kobopatch_save_file_path = os.path.join(save_folder, kobopatch_file_name)

        checkbox_state = kobopatch_checkbox.isChecked()

        try: 
            with open(kobopatch_save_file_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)

            overrides = data.get('overrides')
            for file_name in overrides:
                if target_file_name in file_name:
                    options = overrides.get(file_name)
                    if options:
                        for option in options:
                            if target_option in option:         
                                options[option] = checkbox_state #write new state 
                                break
            with open(kobopatch_save_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)
        except Exception as e:
            configSettings.log(self, "Error kobopatch.yaml: "+str(e))
            self._view.tab_widget.savedpatches_info_label.setText("Error: "+str(e))
    
    def kobopatch_remove_all(self):
        #remove all patches from save kobopatch.yaml
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Remove all")
        msg_box.setText("Remove all backed up patches?")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        result = msg_box.exec()
        if result == QMessageBox.StandardButton.Cancel:
            return

        app_folder = str(configSettings(self._settings).app_folder)
        save_folder_name = "kobopatch_save"
        save_folder = os.path.join(app_folder, save_folder_name)
        kobopatch_file_name = "kobopatch.yaml"
        kobopatch_save_file_path = os.path.join(save_folder, kobopatch_file_name)
        kobopatch_unsave_file_path = os.path.join(app_folder, kobopatch_file_name)

        try: 
            with open(kobopatch_save_file_path, encoding='utf-8') as f:
                data_save = yaml.safe_load(f)
            with open(kobopatch_unsave_file_path, encoding='utf-8') as stream:
                data_unsave = yaml.safe_load(stream)

            overrides_unsave = data_unsave.get('overrides')
            overrides_save = data_save.get('overrides')

            # delete from save
            for file_name_save in overrides_save:
                options_save = overrides_save.get(file_name_save)
                if options_save:
                    for option_save in list(options_save.keys()):
                        del options_save[option_save]

            # delete from unsave
            for file_name_unsave in overrides_unsave:
                options_unsave = overrides_unsave.get(file_name_unsave)
                if options_unsave:
                    for option_unsave in list(options_unsave.keys()):
                        del options_unsave[option_unsave]
                            
            with open(kobopatch_save_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data_save, f)
            with open(kobopatch_unsave_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data_unsave, f)
            
            self.loadKobopatchFile()
        except Exception as e:
            configSettings.log(self, "Error kobopatch.yaml: "+str(e))
            self._view.tab_widget.savedpatches_info_label.setText("Error: "+str(e))
    
    def kobopatch_activate_all(self):
        # deselect all checkboxes
        for checkbox, file_name, patch_name in self.kobopatch_checkboxes:
            if not checkbox.isChecked():
                checkbox.setChecked(True) #to checked
              # self.kobopatch_checkbox_state_changed(file_name, patch_name, checkbox, -1)

    def kobopatch_deactivate_all(self):
        # deselect all checkboxes
        for checkbox, file_name, patch_name in self.kobopatch_checkboxes:
            if checkbox.isChecked():
                checkbox.setChecked(False) #to unchecked
              # self.kobopatch_checkbox_state_changed(file_name, patch_name, checkbox, -1)