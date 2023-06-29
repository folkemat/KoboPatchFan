from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QGroupBox, QTextEdit,QSizePolicy, QScrollArea


def _createStatusSite(self):

    generalStatusSiteLayout = QVBoxLayout()
    
    self.statusSiteGroupbox = QGroupBox()
    self.statusSiteGroupbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

    """Create the layout of the box"""
    vbox = QVBoxLayout() 
    self.statusSiteGroupbox.setLayout(vbox)

    """Create and add the label to the box"""
    self.statusSiteLabel = QLabel()
    self.statusSiteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.statusSiteLabel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    self.statusSiteLabel.setStyleSheet('background-color: white;border: 2px solid gray;')
    self.statusSiteLabel.setText("<h3>Log</h3>")

    self.log_text = QTextEdit()
    self.log_text.setReadOnly(True)  # Set the text widget as read-only

    self.log_text.append("Log initiated")

    """FINAL ADD: Add item by item"""
    #1. label
    vbox.addWidget(self.statusSiteLabel)
    vbox.addWidget(self.log_text)

    """Add groupbox TO workingdir-layout"""
    self.log_box_layout.addWidget(self.statusSiteGroupbox)
    """Add  workingdir-layout TO tab1-layout"""
    self.tab5.layout.addLayout(generalStatusSiteLayout)
    vbox.addStretch(1)
    generalStatusSiteLayout.addStretch(1)