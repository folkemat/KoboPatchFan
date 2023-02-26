#Filename: editorClass.py
import sys
import subprocess
import os
from configSettingsClass import configSettings
from loadDataThreadClass import LoadDataThread
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPlainTextEdit, QGroupBox, QPushButton, QVBoxLayout, QCheckBox, QTextEdit, QHBoxLayout, QWidget
from functools import partial

class editor:
    def __init__(self, settings, view):
        super().__init__()
        self._settings = settings
        self._view = view
        
        self.editor_text = ""
        self.checkboxes = []
        self.choosenFileTab = 0
        self.buildThreadDone = True

    def colorfulTabs(self, index):
        #Here the tabs, which are actually buttons, are made to look like tabs
        
        buttons = [self._view.tab_widget.tab1_button, self._view.tab_widget.tab2_button, self._view.tab_widget.tab3_button, self._view.tab_widget.tab4_button]
        
        selected_style = "background-color: #f0f0f0; border-top-left-radius: 4px; border-top-right-radius: 4px; border: 1px solid #ccc; border-bottom: 1px solid #f0f0f0; padding: 6px 10px; height: 30px;"
        unselected_style = "border: 1px solid #C2C7CB; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom: none; padding: 4px 16px; background-color: #EFEFEF;color: #676767; height: 30px;"
        
        for i, button in enumerate(buttons):
            if i == index:
                button.setStyleSheet(selected_style)
            else:
                button.setStyleSheet(unselected_style)

    def switchTab(self, index):
        #This is called from outside (controller) as soon a tab is changed
        if self.buildThreadDone == True:
            self.choosenFileTab = index #so that we know the tba
            self.reloadFile() #reload the file and build gui
        else:
            pass

    def whichFileToLoad(self):
        #Here we calculate which file we want to load based on which tab(button) is currently selected

        index = self.choosenFileTab 
        homePath = str(configSettings.getSetting(self, "working_dir"))
        src_path = os.path.join(homePath, "src")
        filename = "Unknown"

        if index == 0: #first ab
            filename = configSettings.getSetting(self, "filename_nickel")
        elif index == 1: #second tab
            filename = configSettings.getSetting(self, "filename_libnickel")
        elif index == 2: #3. tab
            filename = configSettings.getSetting(self, "filename_librmsdk")
        elif index == 3: #4. tab
            filename = configSettings.getSetting(self, "filename_libadobe")

        file_path = os.path.join(src_path, filename)
        return file_path
    
    def on_text_edit_changed(self):
        #If the user changes the text in PlaintextEdit in the Open Edit Menu, then the text is saved here
        self.editor_text = self.more_edit.toPlainText()

    def createMoreMenu(self, checkbox_label, checkbox, desc_text, more_text):
        #This is the so-called Open Edit Mode
        
        # We build it by removing the overview with the checkboxes ...
        self.clearLayout(self._view.tab_widget.chkBoxLayout)

        # ... and then by creating a groupbox with a PlainTextEdit
        self.more_edit = QPlainTextEdit(more_text)
        self.more_edit.setReadOnly(False)
        self.more_edit.textChanged.connect(self.on_text_edit_changed) #Absolutely every change is saved

        #Layout
        self.more_edit_layout = QVBoxLayout()
        self.more_edit_layout.addWidget(self.more_edit)

        #Button to bring us back to overview while saving
        self.back_button = QPushButton("<- Back (Save)")
        self.back_button.clicked.connect(partial(self.saveAndReloadFile, more_text))

        #Button for a very simple method to undo changes
        self.restore_button = QPushButton("Restore saved")
        self.restore_button.clicked.connect(partial(self.on_restore_default_clicked, more_text))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.restore_button)
        
        groupbox = QGroupBox(checkbox_label)
        groupbox_layout = QVBoxLayout()
        
        #Warning because changes can prevent file from being read
        warning_label = QLabel("Warning: Edit the following code only if you know what you are doing! Incorrect modifications can prevent the entire file from being processed.")
        warning_label.setStyleSheet('color:red; font-weight:bold')
        warning_label.setWordWrap(True)
        groupbox_layout.addWidget(warning_label)
        
        groupbox_layout.addLayout(self.more_edit_layout)
        groupbox_layout.addLayout(button_layout)
        groupbox.setLayout(groupbox_layout)

        #Create a new QVBoxLayout layout containing the groupbox widget and add it to the chkBoxLayout
        vbox = QVBoxLayout()
        vbox.addWidget(groupbox)
        self._view.tab_widget.chkBoxLayout.addLayout(vbox)

    def on_restore_default_clicked(self, more_text):
        # Implement the logic to restore the default value
        self.more_edit.setPlainText(more_text)

    def saveAndReloadFile(self, more_text):
        #Here, changes from the Open Edit Mode are written to the file.
        
        file_path = self.whichFileToLoad()

        #Old and new text:
        new_text = self.editor_text #Read out updated text from the editor
        old_text = more_text

        if len(new_text) > 0: #0 means that there have been no changes and nothing needs to be written
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                #In the file-content, replace old_text with new_text    
                contentText = text
                contentText = contentText.replace(old_text, new_text)

                #Write back into file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(contentText)

            except Exception as e:
                self._view.tab_widget.label_edit_filename.setText("Error: Can not write file!")
                configSettings.log(self, "Error saveAndReloadFile: Can not read/write file!: "+str(e))
                return

        #Reload file to come back to the Overview
        self.reloadFile()

    def clearLayout(self, layout):
        #Here, all layout and widgets and the variables are cleared (for a reload)
        #in order to make room for new ones
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child.layout())
        self.checkboxes = []
        self.editor_text = ""
        self._view.tab_widget.search_edit.setText("")

    def handle_data_loaded(self, patch_numbers, file_path):
        #This function is called when the thread is finished
        #and only serves to update the label
        filename = os.path.basename(file_path)
        self._view.tab_widget.label_edit_filename.setText("File: "+str(filename)+" | Patches: "+str(patch_numbers)+" | ")
        self.buildThreadDone = True

    def reloadFile(self):
        #Here the file is read in and processed and the layout is created based on it

        # First, remove all widgets from the chkBoxLayout and clear everthing
        self.clearLayout(self._view.tab_widget.chkBoxLayout)

        #Choose which file to load
        choosenTab = self.choosenFileTab
        file_path = self.whichFileToLoad()
        #Refresh tabs
        self.colorfulTabs(choosenTab)

        #Processing the patch file
        try:
            if not os.path.isfile(file_path) or not file_path.endswith('.yaml'):
                self._view.tab_widget.label_edit_filename.setText("Error: File not found!")
                configSettings.log(self, "Error ReloadFile: File .yaml not found!")
                return
            #Create a thread in which the data for the widgets is calculated 
            self.buildThreadDone = False
            self.load_thread = LoadDataThread(file_path)
            self.load_thread.create_patches_components.connect(self.create_patch_gui) #This is called for every patch option found
            self.load_thread.data_loaded.connect(self.handle_data_loaded) #When everything is loaded and set up
            self.load_thread.start()
        except Exception as e:
            self._view.tab_widget.label_edit_filename.setText("Error: Can not read file! If you have corrupted the file, download it again.")
            configSettings.log(self, "Error Editor: Can not read patch file!: "+str(e))
            return

    def create_patch_gui(self, checkbox_label, checkbox_state, desc_text, more_text, patch_group_text, number_of_patch, file_path):        
        #create checkbox, desc box, more edit button etc. here and insert it in the layout

        checkbox = QCheckBox(checkbox_label)
        checkbox.setChecked(checkbox_state)
        checkbox.stateChanged.connect(partial(self.checkbox_state_changed, checkbox)) #connect all checkboxes
        
        #fancy new font
        current_font = checkbox.font()
        current_size = current_font.pointSize()
        new_font = QFont(current_font.family(), current_size + 1, QFont.Weight.Bold)
        checkbox.setFont(new_font)

        #desc box under checkbox
        desc_text_edit = QTextEdit(desc_text)
        desc_text_edit.setReadOnly(True)
        #desc_text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        desc_text_layout = QVBoxLayout()  
        desc_text_layout.addWidget(desc_text_edit)
        desc_text_layout.setContentsMargins(0, 0, 0, 0)
        desc_text_layout.addWidget(QWidget(), stretch=1)

        #open edit mode button under desc
        more_button = QPushButton("Open Edit Mode")
        more_button.clicked.connect(partial(self.createMoreMenu, checkbox_label, checkbox, desc_text, more_text))
        
        #label above checkbox for checkbox
        group_label = QLabel("No. "+str(number_of_patch)+" | Group: "+patch_group_text)
        group_label.setWordWrap(True)

        #layout things
        groupbox = QGroupBox()
        groupbox_layout = QVBoxLayout()
        groupbox_layout.addWidget(group_label)
        groupbox_layout.addWidget(checkbox)
        groupbox_layout.addLayout(desc_text_layout)
        groupbox_layout.addWidget(more_button)
        groupbox.setLayout(groupbox_layout)
        
        #inset into layout
        last_index = self._view.tab_widget.chkBoxLayout.count() 
        self._view.tab_widget.chkBoxLayout.insertWidget(last_index, groupbox)
        self._view.tab_widget.label_edit_filename.setText("Loading patch "+str(number_of_patch)+" ... ")

        #for later use, save the checkboxes
        self.checkboxes.append([checkbox, groupbox, patch_group_text, number_of_patch])
    
    def checkbox_state_changed(self, checkbox, index):
        #change the file according to checkbox state
        label = checkbox.text()
        state = checkbox.isChecked()
        file_path = self.whichFileToLoad()
        try:
            #Open file
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            #Finding the lines that need to be updated
            i = 0
            while i < len(lines):
                if label in lines[i]:
                    if "Enabled: yes" in lines[i+1] and not state:
                        lines[i+1] = "  - Enabled: no\n"
                    elif "Enabled: no" in lines[i+1] and state:
                        lines[i+1] = "  - Enabled: yes\n"
                    break
                i += 1
            
            # Write the updated lines back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
        except Exception as e:
            self._view.tab_widget.label_edit_filename.setText("Error: Cannot change checkbox state!")
            configSettings.log(self, "Error: Cannot change checkbox state: "+str(e))
            return
    
    def deselect_checkboxes(self):
        # deselect all checkboxes
        for checkbox, groupbox, patch_group_text, number_of_patch in self.checkboxes:
            if checkbox.isChecked():
                checkbox.setChecked(False) #to unchecked
                self.checkbox_state_changed(checkbox, -1) #write change in file

    def openFolderSrc(self):
        try:
            path = str(configSettings.getSetting(self, "working_dir"))
            folder_path = os.path.join(path, "src")
            if sys.platform == "win32":
                os.startfile(folder_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, folder_path])
                
        except Exception as e:
            self._view.tab_widget.label_edit_filename.setText("Error: Cannot open folder src!")
            configSettings.log(self, "Error: Cannot open folder src: "+str(e))
            return


    def filter_checkboxes(self):
        # Die Sucheingabe des Benutzers abrufen
        search_text = self._view.tab_widget.search_edit.text().lower()
        
        # Alle Checkboxen durchgehen und nur noch passende anzeigen
        for checkbox, groupbox, patch_group_text, number_of_patch in self.checkboxes:
            label_text = checkbox.text().lower()
            if search_text in label_text:
                groupbox.show()
            else:
                groupbox.hide()