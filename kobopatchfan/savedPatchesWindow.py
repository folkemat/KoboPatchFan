from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGroupBox, QLineEdit, QListWidget

def _createSavedPatches(self):
    groupBox = QGroupBox()

    self.listWidget = QListWidget()
    self.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection) 
    self.listWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    self.saved_patches_layout = QVBoxLayout()

    self.savedpatches_info_label = QLabel()
    self.kobopatch_save_location = QLineEdit()
    self.kobopatch_save_location.setReadOnly(True)
    infoLayout = QHBoxLayout()
    infoLayout.addWidget(self.savedpatches_info_label)
    infoLayout.addWidget(self.kobopatch_save_location)
    self.saved_patches_layout.addLayout(infoLayout)

    self.saved_patches_layout.addWidget(self.listWidget)
    groupBox.setLayout(self.saved_patches_layout)

    # Controls
    self.kobopatch_reload_button = QPushButton("Reload")
    self.kobopatch_deactivate_all_button = QPushButton("Disable All")
    self.kobopatch_activate_all_button = QPushButton("Enable All")
    self.kobopatch_remove_all_button = QPushButton("Remove all")
    self.savedkobopatch_controlsLayout = QHBoxLayout()
    self.savedkobopatch_controlsLayout.addWidget(self.kobopatch_reload_button)
    self.savedkobopatch_controlsLayout.addStretch()  # add stretchable space to center the buttons
    self.savedkobopatch_controlsLayout.addWidget(self.kobopatch_deactivate_all_button)
    self.savedkobopatch_controlsLayout.addWidget(self.kobopatch_activate_all_button)
    self.savedkobopatch_controlsLayout.addStretch()  # add stretchable space to center the buttons
    self.savedkobopatch_controlsLayout.addWidget(self.kobopatch_remove_all_button)
    self.saved_patches_layout.addLayout(self.savedkobopatch_controlsLayout)

    # Add group box to tab 4 layout
    self.tab4.layout.addWidget(groupBox)