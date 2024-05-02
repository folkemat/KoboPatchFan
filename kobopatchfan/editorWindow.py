# Filename: editorWindow.py

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLineEdit, QWidget,QScrollArea, QGraphicsDropShadowEffect)

def _createEditor(self):
    
    # Create a QWidget to hold the buttons
    self.tab_buttons_widget = QWidget()
    self.tab_buttons_layout = QHBoxLayout(self.tab_buttons_widget)
    self.tab_buttons_layout.setContentsMargins(0, 0, 0, 0)
    #self.tab_buttons_layout.setSpacing(0)

    # Create the buttons and add them to the layout
    self.tab1_button = QPushButton("nickel")
    self.tab2_button = QPushButton("libnickel")
    self.tab3_button = QPushButton("librmsdk")
    self.tab4_button = QPushButton("libadobe")
    self.tab_buttons_layout.addWidget(self.tab1_button)
    self.tab_buttons_layout.addWidget(self.tab2_button)
    self.tab_buttons_layout.addWidget(self.tab3_button)
    self.tab_buttons_layout.addWidget(self.tab4_button)

    # Create the editor widgets
    self.label_and_search_layout = QHBoxLayout()
    self.label_edit_filename = QLabel()
    self.label_and_search_layout.addWidget(self.label_edit_filename)
    self.search_edit = QLineEdit()
    self.search_edit.setPlaceholderText("Search ...")
    self.label_and_search_layout.addWidget(self.search_edit)
    self.save_kobopatch_button = QPushButton("Backup selection")
    self.save_kobopatch_button.setFixedHeight(35)

    # create QGraphicsDropShadowEffect
    shadow_effect = QGraphicsDropShadowEffect(self)
    shadow_effect.setColor(QColor("#FF8C00"))
    shadow_effect.setOffset(0, 0)
    shadow_effect.setBlurRadius(15)
    self.save_kobopatch_button.setGraphicsEffect(shadow_effect)

    self.chkBoxLayout = QVBoxLayout()
    self.chkBoxLayout.addStretch(1) 
    self.chkBoxLayout.setContentsMargins(0,0,0,0)
    self.chkBoxLayout.setSpacing(0) 
    self.scroll_area_widget = QWidget()
    self.scroll_area_widget.setLayout(self.chkBoxLayout)
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)         
    self.scroll_area.setWidget(self.scroll_area_widget) 
    self.control_box = QGroupBox()
    self.control_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.save_label = QLabel("Note: Changes are automatically saved")
    self.show_selected_button = QPushButton("Show only selected")
    self.show_selected_button.setFixedHeight(35)
    self.reload_button = QPushButton("Reload")
    self.reload_button.setFixedHeight(35)
    self.deselect_button = QPushButton("Deselect all")
    self.deselect_button.setFixedHeight(35)
    self.open_src_button = QPushButton("Open Folder")
    self.open_src_button.setFixedHeight(35)

    self.control_layout = QHBoxLayout()
    self.control_layout.addWidget(self.show_selected_button)
    self.control_layout.addWidget(self.reload_button)
    self.control_layout.addWidget(self.save_kobopatch_button)
    self.control_layout.addWidget(self.deselect_button)
    self.control_layout.addWidget(self.open_src_button)

    self.control_box.setLayout(self.control_layout)

    # Create a QWidget to hold the editor widgets
    self.editor_widget = QWidget()
    self.editor_layout = QVBoxLayout(self.editor_widget)
    self.editor_layout.setContentsMargins(0, 0, 0, 0)
    self.editor_layout.addLayout(self.label_and_search_layout)
    self.editor_layout.addWidget(self.scroll_area)
    self.editor_layout.addWidget(self.control_box)
    self.editor_layout.addWidget(self.save_label)

    """Add QTabWidget TO tab2-layout"""
    self.tab2.layout.addWidget(self.tab_buttons_widget)
    self.tab2.layout.addWidget(self.editor_widget)