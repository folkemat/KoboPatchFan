from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QRadioButton, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGroupBox, QSizePolicy

def _createWorkingDir(self):

    generalWorkingDirLayout = QHBoxLayout()
    self.workingDirGroupbox = QGroupBox()
    self.workingDirGroupbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.workingDirGroupbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    """Create the layout of the box"""
    vbox = QVBoxLayout()
    self.workingDirGroupbox.setLayout(vbox)

    """Create and add the buttons to the box"""
    self.changeWorkingDirButton = QPushButton('Change working directory...')
    self.applyWorkingDirButton = QPushButton('Save')
    self.doneWorkingDirButton = QPushButton('Done')

    """Create and add the label to the box"""
    self.workingDirLabel = QLabel()
    #self.workingDirLabel.setWordWrap(True)
    self.firstStepLabel = QLabel()
    self.firstStepLabel.setWordWrap(True)
    self.firstStepLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.firstStepLabel.setText("<h3>Working directory</h3>")
    self.firstStepLabel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    self.firstStepLabel.setStyleSheet('background-color: white;border: 2px solid gray;')

    """Create and add the inform-radio to the box"""
    self.createFolderRadiobutton = QRadioButton("Use folder 'KoboPatchFan' as working-folder")
    self.createFolderRadiobutton.setChecked(True)
    self.createFolderRadiobutton.setEnabled(False)

    """Create and add the open folder button to the box"""
    self.openFolderButton = QPushButton('Open folder')
    self.openFolderButton.setFixedHeight(50)

    """FINAL ADD: Add item by item"""
    # 0. Explain-label
    vbox.addWidget(self.firstStepLabel)
    # 1. done button
    vbox.addWidget(self.doneWorkingDirButton, alignment=Qt.AlignmentFlag.AlignCenter)
    # 2. working dir path label
    vbox.addWidget(self.workingDirLabel, alignment=Qt.AlignmentFlag.AlignCenter)
    # 3. change button
    vbox.addWidget(self.changeWorkingDirButton, alignment=Qt.AlignmentFlag.AlignCenter)
    # 4. radiobutton about folder-name
    vbox.addWidget(self.createFolderRadiobutton)
    # 5. open folder button
    vbox.addWidget(self.openFolderButton)

    self.tab4left_half.addWidget(self.workingDirGroupbox)
    self.tab4.layout.addLayout(generalWorkingDirLayout)
    generalWorkingDirLayout.addStretch(1)
    vbox.addStretch(1)