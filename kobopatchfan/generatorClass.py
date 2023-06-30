#Filename: generatorClass.py

import sys
import subprocess
import os
import platform
from configSettingsClass import configSettings
from processThreadClass import ProcessThread
from loadDataThreadClass import LoadDataThread
from checkerClass import checkerClass
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QFileDialog, QTextEdit, QVBoxLayout, QDialog, QPushButton
import shutil
import yaml
import re

class ScrollableTextDialog(QDialog):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("All activated patches")
        
        text_edit = QTextEdit()
        text_edit.setHtml(text)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        ok_button = QPushButton("Close")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

class generator:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        self._process = None
        self.process_success = False
    
    def show_info_dialog(self):
        homePath = str(configSettings(self._settings).app_folder)
        self.load_thread = LoadDataThread(homePath, 2)
        self.load_thread.finish_all_patches.connect(self.show_all_patches)
        self.load_thread.start()

    def show_all_patches(self, all_patches):
        numberOfPatch = 0
        count = 0
        msg_text = ""
        try:
            for patch in all_patches:
                numberOfPatch += 1
                patch_name = patch[0]
                patch_state = patch[1]
                filename = patch[2]
                if patch_state:
                    count = count+1
                    msg_text += f"No. {numberOfPatch}: <b>{patch_name}</b> (in {filename})<br><br>"
        except Exception as e:
                configSettings.log(self, "Error show_all_patches: "+str(e))

        scrollable_text = f"<html><body>You have activated <b>{str(count)}</b> patches:<br><br>{msg_text}</body></html>"
        dialog = ScrollableTextDialog(scrollable_text)
        dialog.exec()

    def runScript(self):
        homePath = str(configSettings(self._settings).app_folder)
        #reset output
        self._view.tab_widget.gen_plainTextEdit.setStyleSheet("color: none")
        self._view.tab_widget.gen_plainTextEdit.clear()
        self._view.tab_widget.export_button.setEnabled(False)
        #this will write kobopatch.yaml
        self.use_kobopatch(self._view.tab_widget.use_kobopatch_checkbox.isChecked())
        self.process_success = False
        
        if platform.system() == 'Windows':
            file_name = 'kobopatch.bat'
            command = ['cmd', '/c', os.path.join(homePath, file_name)]
            configSettings.log(self, "Found Windows, using cmd to run kobopatch.bat")
        elif platform.system() == 'Linux':
            file_name = 'kobopatch.sh'
            command = ['bash', os.path.join(homePath, file_name)]
            configSettings.log(self, "Found Linux, using bash to run kobopatch.sh")
        else:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText('This operating system is not supported!')
            configSettings.log(self, "Error: Cannot run script: This operating system is not supported!")
            return

        #start the process
        self.process_thread = ProcessThread(command)
        self.process_thread.finished.connect(self.on_process_finished)
        self.process_thread.errorChanged.connect(self.on_ready_read)
        self.process_thread.outputChanged.connect(self.on_ready_read)
        self.process_thread.start()

        self._view.tab_widget.gen_plainTextEdit.insertPlainText(f"Execution of {file_name} started ...\n")
        configSettings.log(self, "Started execution of run script")
        self._view.tab_widget.run_button.setEnabled(False)

    def on_ready_read(self, output):
        data_str = output
        if data_str:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText(data_str)
            self._view.tab_widget.gen_plainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
            self._view.tab_widget.gen_plainTextEdit.ensureCursorVisible()

    def on_process_finished(self, exitCode):
        if exitCode == 0:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText("\nExecution successful.\n\n")
            configSettings.log(self, "Execution of script successful.")
        elif exitCode == 62097:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText(f"\nExecution successful. (Exit Code: {exitCode}).\n\n")
            configSettings.log(self, "Execution of script successful but process killed because of windows-waiting-60-secs.")
        elif exitCode != 0:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText(f"\nExecution failed (Exit Code: {exitCode}).\n\n")
            configSettings.log(self, "Execution of script failed.")
        else:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText("\nExecution terminated unexpectedly.\n\n")
        self._view.tab_widget.gen_plainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        self._view.tab_widget.gen_plainTextEdit.ensureCursorVisible()
        self._view.tab_widget.run_button.setEnabled(True)
        #if process finished successfully, show export options
        self.showExport()

    def showExport(self):
        path = str(configSettings(self._settings).app_folder)
        file_path = os.path.join(path, "out")
        filename = "KoboRoot.tgz"
        final_file_path = os.path.join(file_path, filename)
        self._view.tab_widget.export_plainTextEdit.clear()
        self._view.tab_widget.export_plainTextEdit.insertPlainText(final_file_path)
        self._view.tab_widget.export_button.setEnabled(True)

        configSettings.log(self, "Generated KoboRoot.tgz at "+str(final_file_path))
    
    def openFolderOut(self):
        try:
            path = str(configSettings(self._settings).app_folder)
            folder_path = os.path.join(path, "out")
            if sys.platform == "win32":
                os.startfile(folder_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, folder_path])
        except Exception as e:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText("Open File Error: "+str(e))
            self._view.tab_widget.gen_plainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
            self._view.tab_widget.gen_plainTextEdit.ensureCursorVisible()
            configSettings.log(self, "Open File Error: "+str(e))

    def doTheExport(self):
        path = str(configSettings(self._settings).app_folder)
        file_path = os.path.join(path, "out")
        filename = "KoboRoot.tgz"
        final_file_path = os.path.join(file_path, filename)
        if self.check_file_exists(final_file_path):
            dest_path = self.browse_save_location()
            if dest_path:
                # Try to save the file
                try:
                    shutil.copy2(final_file_path, dest_path)
                    # Show a success message if the file is saved
                    self._view.tab_widget.gen_plainTextEdit.insertPlainText("\nExported "+final_file_path+" to "+dest_path)
                except Exception as e:
                    # Show an error message if the file cannot be saved
                    self._view.tab_widget.gen_plainTextEdit.insertPlainText("\nError while exporting file "+final_file_path+" to "+dest_path+": "+ str(e))
                    self._view.tab_widget.gen_plainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
                    self._view.tab_widget.gen_plainTextEdit.ensureCursorVisible()
                    configSettings.log(self, "Export Error: Error while exporting file "+final_file_path+" to "+dest_path+": "+ str(e))
            else:
                self._view.tab_widget.gen_plainTextEdit.insertPlainText("Export Error: Please select a save location for "+final_file_path)
                self._view.tab_widget.gen_plainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
                self._view.tab_widget.gen_plainTextEdit.ensureCursorVisible()
                configSettings.log(self, "Export Error: Could not find save location for "+final_file_path)
        else:
            self._view.tab_widget.gen_plainTextEdit.insertPlainText("\nError: File does not exist at "+final_file_path)
            self._view.tab_widget.gen_plainTextEdit.moveCursor(QTextCursor.MoveOperation.End)
            self._view.tab_widget.gen_plainTextEdit.ensureCursorVisible()
            configSettings.log(self, "Export Error: File does not exist at "+final_file_path)
    
    def browse_save_location(self):
        save_location = QFileDialog.getExistingDirectory(None, 'Select a folder for KoboRoot.tgz:')
        if save_location:
            return save_location
        else:
            return False

    def check_file_exists(self, file_path):
        if os.path.isfile(file_path):
            return True
        else:
            return False
            
    def use_kobopatch(self, is_checked):
        app_folder = str(configSettings(self._settings).app_folder)
        save_folder_name = "kobopatch_save"
        save_folder = os.path.join(app_folder, save_folder_name)
        kobopatch_file_name = "kobopatch.yaml"
        kobopatch_unsave_file_path = os.path.join(app_folder, kobopatch_file_name)
        kobopatch_save_file_path = os.path.join(save_folder, kobopatch_file_name)
        
        if not is_checked: # delete patches
            try:
                with open(kobopatch_unsave_file_path, encoding='utf-8') as stream:
                    data_unsave = yaml.safe_load(stream)
                with open(kobopatch_save_file_path, encoding='utf-8') as stream:
                    data_save = yaml.safe_load(stream)

                overrides_unsave = data_unsave.get('overrides')
                overrides_save = data_save.get('overrides')
                for file_name_save in overrides_save:
                    options_save = overrides_save.get(file_name_save)
                    for file_name_unsave in overrides_unsave:
                        if file_name_unsave in file_name_save:
                            options_unsave = overrides_unsave.get(file_name_unsave)
                            for option in options_save:
                                if options_unsave:
                                    if option in options_unsave:
                                        del options_unsave[option]
                                        print("Deleted "+option+" from "+file_name_save)
                                    else:
                                        print("Not deleted "+option+" to "+file_name_save)

                with open(kobopatch_unsave_file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data_unsave, f)
            except Exception as e:
                configSettings.log(self, "Error removing patches from save kobopatch.yaml: "+str(e))
                return

        else: #add patches

            #first, write new version to saved kobopatch.yaml
            target_firmware = checkerClass.readKobopatchyaml(self)
            try:
                with open(kobopatch_save_file_path, encoding='utf-8') as stream:
                    data_save = yaml.safe_load(stream)

                pattern = r"\d+\.\d+\.\d+"
                firmware_in = data_save.get("in")
                new_version = re.sub(pattern, target_firmware, firmware_in)
                data_save["in"] = new_version
                data_save["version"] = target_firmware

                with open(kobopatch_save_file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data_save, f)
                    
                #print("Wrote new version: old: "+str(firmware_in)+" new: "+new_version)
            except Exception as e:
                    configSettings.log(self, "Error write new version to saved kobopatch.yaml: "+str(e))
                    return
            
            #second, copy saved patches to unsave_kobopatch.yaml file
            try:
                with open(kobopatch_unsave_file_path, encoding='utf-8') as stream:
                    data_unsave = yaml.safe_load(stream)
                
                overrides_unsave = data_unsave.get('overrides')
                overrides_save = data_save.get('overrides')

                for file_name_save in overrides_save:
                    options_save = overrides_save.get(file_name_save)
                    for file_name_unsave in overrides_unsave:
                        if file_name_unsave in file_name_save:
                            options_unsave = overrides_unsave.get(file_name_unsave)
                            for option in options_save:
                                if not options_unsave:
                                    options_unsave = {}
                                    options_unsave[option] = options_save[option]
                                    overrides_unsave[file_name_unsave] = options_unsave
                                else:
                                    options_unsave[option] = options_save[option] 

                with open(kobopatch_unsave_file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data_unsave, f)
            except Exception as e:
                configSettings.log(self, "Error add patches from save kobopatch.yaml to unsave kobopatch.yaml: "+str(e))
                return
        

