#Filename: generatorClass.py

import sys
import subprocess
import os
import platform
from configSettingsClass import configSettings
from processThreadClass import ProcessThread
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QFileDialog
import shutil

class generator:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        self._process = None
        self.process_success = False

    def runScript(self):
        homePath = str(configSettings.getSetting(self, "working_dir"))
        #reset output
        self._view.tab_widget.gen_plainTextEdit.setStyleSheet("color: none")
        self._view.tab_widget.gen_plainTextEdit.clear()
        self._view.tab_widget.export_button.setEnabled(False)
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
        path = str(configSettings.getSetting(self, "working_dir"))
        file_path = os.path.join(path, "out")
        filename = "KoboRoot.tgz"
        final_file_path = os.path.join(file_path, filename)
        self._view.tab_widget.export_plainTextEdit.clear()
        self._view.tab_widget.export_plainTextEdit.insertPlainText(final_file_path)
        self._view.tab_widget.export_button.setEnabled(True)

        configSettings.log(self, "Generated KoboRoot.tgz at "+str(final_file_path))
    
    def openFolderOut(self):
        try:
            path = str(configSettings.getSetting(self, "working_dir"))
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
        path = str(configSettings.getSetting(self, "working_dir"))
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
            