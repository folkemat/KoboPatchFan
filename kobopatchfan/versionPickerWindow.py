from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGroupBox, QComboBox

def _createVersionPicker(self):
      generalVersionLayout = QHBoxLayout()

      self.generalVersionBox = QGroupBox()
      self.generalVersionBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
      self.generalVersionBox.setStyleSheet("QGroupBox {border: 2px solid grey; border-radius: 5px; margin-top: 1ex;}")

      """Create the layout of the box"""
      vbox = QVBoxLayout() 
      self.generalVersionBox.setLayout(vbox)

      """Create and add the label to the box"""
      self.labelVersionPicker = QLabel()
      self.labelVersionPicker.setText("<h3>Select your firmware</h3>")
      self.labelVersionSelected = QLabel()

      """Create and add the Buttons to the box"""
      #self.buttonUpdateVersions = QPushButton("Re-read versions")
      self.buttonPickLatest = QPushButton("Pick latest version")
      self.buttonPickLatest.setFixedHeight(35)

      """Create and add the combo to the box"""
      self.comboVersions = QComboBox(self)
      self.comboVersions.setMinimumHeight(50)

      """Add widgets to the box"""
      vbox.addWidget(self.labelVersionPicker)
      vbox.addWidget(self.labelVersionSelected)
      vbox.addWidget(self.comboVersions)
      hbox = QHBoxLayout()
      vbox.addLayout(hbox)
      #hbox.addWidget(self.buttonUpdateVersions)
      hbox.addWidget(self.buttonPickLatest)

      self.left_half.addWidget(self.generalVersionBox)
      self.tab1.layout.addLayout(generalVersionLayout)
      vbox.addStretch(1)