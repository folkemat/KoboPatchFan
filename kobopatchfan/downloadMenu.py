from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, QGroupBox, QProgressBar, QCheckBox,QSizePolicy
from PyQt6.QtGui import QColor

def _createDownload(self):

    generalDownloadLayout = QVBoxLayout()
    self.generalDownloadBox = QGroupBox()
    self.generalDownloadBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.generalDownloadBox.setStyleSheet("QGroupBox {border: 2px solid grey; border-radius: 5px; margin-top: 1ex;}")

    """Create the layout of the box"""
    vbox = QVBoxLayout() 
    self.generalDownloadBox.setLayout(vbox)

    """Create and add the label to the box"""
    self.labelDownload = QLabel()
    self.labelDownload.setText("<h3>Download the required files</h3>")
    self.labelDownload.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.labelDownload.setWordWrap(True)
    #self.labelDownload.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    self.labelDownloadInfo = QLabel()
    self.labelDownloadInfo.setText("Make sure you have selected your firmware and Kobo correctly!")
    self.labelDownloadInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.labelDownloadInfo.setWordWrap(True)
    #self.labelDownloadInfo.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    """Create and add the Buttons to the box"""
    self.buttonDownloadPauseResume = QPushButton("Pause")
    self.buttonDownloadCancel = QPushButton("Cancel")
    self.buttonDownloadCancel.setEnabled(False)
    self.buttonDownloadPauseResume.setEnabled(False)

    self.checkBoxExtract = QCheckBox(self)
    self.checkBoxExtract.setEnabled(True)
    self.checkBoxExtract.setChecked(True)
    self.checkBoxExtract.setText("Extract files after download (important!)")

    self.label_speed = QLabel("Speed:", self)
    self.label_speed.setWordWrap(True)
    self.label_remaining = QLabel("Remaining:", self)
    self.label_remaining.setWordWrap(True)
    self.label_size = QLabel("Size:", self)
    self.label_size.setWordWrap(True)

    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setValue(0)

    self.downloadStart_button = QPushButton("Start")
    # create QGraphicsDropShadowEffect
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(10)
    shadow_effect.setColor(QColor("#FF8C00"))
    shadow_effect.setOffset(0, 0)
    shadow_effect.setBlurRadius(15)
    self.downloadStart_button.setGraphicsEffect(shadow_effect)

    #adding one by one
    vbox.addWidget(self.labelDownload)
    vbox.addStretch()
    vbox.addWidget(self.downloadStart_button, 0, Qt.AlignmentFlag.AlignHCenter)
    vbox.addWidget(self.labelDownloadInfo)
    vbox.addWidget(self.checkBoxExtract)
    vbox.addWidget(self.label_speed)
    vbox.addWidget(self.label_remaining)
    vbox.addWidget(self.label_size)
    vbox.addWidget(self.progress_bar)
    vbox.addStretch()
    hbox = QHBoxLayout()
    hbox.addWidget(self.buttonDownloadPauseResume)
    hbox.addWidget(self.buttonDownloadCancel)
    vbox.addLayout(hbox)

    self.right_half.addWidget(self.generalDownloadBox)
    self.tab1.layout.addLayout(generalDownloadLayout)
    vbox.addStretch(1)