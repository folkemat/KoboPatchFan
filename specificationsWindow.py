from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QGroupBox, QComboBox, QSizePolicy

def _createSpecifications(self):

    generalSpeciLayout = QHBoxLayout()

    self.speciGroupbox = QGroupBox()
    self.speciGroupbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.speciGroupbox.setStyleSheet("QGroupBox {border: 2px solid grey; border-radius: 5px; margin-top: 1ex;}")

    """Create the layout of the box"""
    vbox = QVBoxLayout() 
    #vbox.setContentsMargins(20, 20, 20, 20)
    #vbox.setSpacing(15)
    self.speciGroupbox.setLayout(vbox)

    """Create the combo box"""
    self.combo = QComboBox(self)
    self.combo.setMinimumHeight(50)
    self.combo.setEditable(False) 
    self.combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert) 

    """Create and add the label to the box"""
    self.labelKoboNames = QLabel()
    self.labelKoboNames.setText("<h3>Select your Kobo</h3>")
    self.labelSelectedKobo = QLabel()

    #adding one by one
    vbox.addWidget(self.labelKoboNames)
    vbox.addWidget(self.labelSelectedKobo)
    vbox.addWidget(self.combo)

    self.left_half.addWidget(self.speciGroupbox)
    self.tab1.layout.addLayout(generalSpeciLayout)
    vbox.addStretch(1)