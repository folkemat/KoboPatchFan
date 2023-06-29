from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGroupBox

def _createUpdateDb(self):

    generalUpdateDbLayout = QHBoxLayout()

    self.updateDbGroupbox = QGroupBox()
    self.updateDbGroupbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.updateDbGroupbox.setAutoFillBackground(True)

    """Create the layout of the box"""
    vbox = QVBoxLayout() 
    self.updateDbGroupbox.setLayout(vbox)

    """Create and add the label to the box"""
    self.labelUpdateDb = QLabel()
    self.labelUpdateDb.setText("<h3>Update database</h3>")
    self.labelUpdateDb.setWordWrap(True)

    self.labelUpdateDbStatus = QLabel()
    self.labelUpdateDbStatus.setText("Status: Not updated")
    self.labelUpdateDbStatus.setWordWrap(True)

    self.labelUpdateDbLastTime = QLabel()
    self.labelUpdateDbLastTime.setText("Click Update to update the database.")
    self.labelUpdateDbLastTime.setWordWrap(True)

    self.labelUpdateDbLatest = QLabel()
    self.labelUpdateDbLatest.setText("Critical: Update database to continue!")
    self.labelUpdateDbLatest.setStyleSheet('color:red; font-weight:bold')
    self.labelUpdateDbLatest.setWordWrap(True)

    """Create and add the Buttons to the box"""
    self.buttonUpdateDb = QPushButton('Update database')

    # adding one by one
    vbox.addWidget(self.labelUpdateDb)
    vbox.addWidget(self.labelUpdateDbStatus)
    vbox.addWidget(self.labelUpdateDbLastTime)
    vbox.addWidget(self.labelUpdateDbLatest)
    vbox.addWidget(self.buttonUpdateDb)

    self.left_half.addWidget(self.updateDbGroupbox)
    self.tab1.layout.addLayout(generalUpdateDbLayout)
    vbox.addStretch(1)