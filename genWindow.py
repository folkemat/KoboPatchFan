# Filename: editorWindow.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QPlainTextEdit, QCheckBox)

def _createGenerator(self):
    
    self.genGroupBox = QGroupBox()

    self.gen_plainTextEdit = QPlainTextEdit()
    self.gen_plainTextEdit.setReadOnly(True)
    self.gen_plainTextEdit.setPlaceholderText("The output will appear here ...")

    self.use_kobopatch_checkbox = QCheckBox("Use Backup-Patches")

    self.run_button = QPushButton('Run')
    self.run_button.setFixedHeight(50)
    self.run_button.setFixedWidth(200)

    self.gen_layout = QVBoxLayout()
    #self.gen_layout.addWidget(saved_patches_groupbox)
    self.gen_layout.addWidget(self.use_kobopatch_checkbox)
    self.gen_layout.addWidget(self.gen_plainTextEdit)
    self.gen_layout.addWidget(self.run_button, 0, Qt.AlignmentFlag.AlignHCenter)
    self.genGroupBox.setLayout(self.gen_layout)

    self.exportGroupBox = QGroupBox("Copy the 'KoboRoot.tgz' file to the '.kobo' folder of your Kobo!")
    self.exportGroupBox.setFixedHeight(90)

    self.export_plainTextEdit = QPlainTextEdit()
    self.export_plainTextEdit.setReadOnly(True)
    self.export_plainTextEdit.setPlaceholderText("The file path will appear here ...")
    self.export_plainTextEdit.setMaximumHeight(50)

    self.open_folder_button = QPushButton('Open Folder')
    self.open_folder_button.setEnabled(True)
    self.open_folder_button.setFixedHeight(50)
    self.open_folder_button.setFixedWidth(100)

    self.export_button = QPushButton('Export File')
    self.export_button.setEnabled(False)
    self.export_button.setFixedHeight(50)
    self.export_button.setFixedWidth(100)

    self.export_layout = QHBoxLayout()
    self.export_layout.addWidget(self.export_plainTextEdit)
    self.export_layout.addWidget(self.open_folder_button)
    self.export_layout.addWidget(self.export_button)
    self.exportGroupBox.setLayout(self.export_layout)

    self.tab3.layout.addWidget(self.genGroupBox)
    self.gen_layout.addWidget(self.exportGroupBox)