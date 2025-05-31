from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QGroupBox, QCheckBox, QPushButton

def _createVerify(self):

    generalVerifyLayout = QHBoxLayout()

    self.verifyGroupbox = QGroupBox()
    self.verifyGroupbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.verifyGroupbox.setStyleSheet("QGroupBox {border: 2px solid grey; border-radius: 5px; margin-top: 1ex;}")

    """Create the layout of the box"""
    vbox = QVBoxLayout() 
    self.verifyGroupbox.setLayout(vbox)

    """Create and add the label to the box"""
    self.labelVerify = QLabel()
    self.labelVerify.setText("<h3>Verify your configuration</h3>")

    self.label_kobo = QLabel("Kobo: ")
    self.label_firmware = QLabel("Firmware: ")
    self.label_kobo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.label_firmware.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.label_kobo.setStyleSheet("border: 2px solid #c6c6c6; padding: 8px;")
    self.label_firmware.setStyleSheet("border: 2px solid #c6c6c6; padding: 8px;")

    self.labelVerifyResult = QLabel()
    self.labelVerifyResult.setText("Not yet verified")
    self.labelVerifyResult.setWordWrap(True)

    self.labelPatchAnywayResult = QLabel()
    self.labelPatchAnywayResult.setText("")
    self.labelPatchAnywayResult.setWordWrap(True)

    # Checkbox option if no patch is found
    self.checkbox_patch_anyway = QCheckBox("Patch anyway")
    self.checkbox_patch_anyway.setStyleSheet("color: green; font-weight: bold;")
    self.checkbox_patch_anyway.hide()

    self.button_patch_anyway_help = QPushButton("?")
    self.button_patch_anyway_help.setFixedWidth(25) 
    self.button_patch_anyway_help.hide() 

    # Checkbox + Button layout
    patchAnywayLayout = QHBoxLayout()
    patchAnywayLayout.addWidget(self.checkbox_patch_anyway)
    patchAnywayLayout.addWidget(self.button_patch_anyway_help)
    patchAnywayLayout.addStretch()

    #adding one by one
    vbox.addWidget(self.labelVerify)
    vbox.addWidget(self.label_kobo)
    vbox.addWidget(self.label_firmware)
    vbox.addWidget(self.labelVerifyResult)
    vbox.addWidget(self.labelPatchAnywayResult)
    vbox.addLayout(patchAnywayLayout)

    self.right_half.addWidget(self.verifyGroupbox)
    self.tab1.layout.addLayout(generalVerifyLayout)
    vbox.addStretch(1)