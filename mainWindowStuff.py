# Filename: mainWindowStuff.py

from PyQt6.QtWidgets import  QHBoxLayout, QMainWindow, QTextEdit, QTabWidget, QVBoxLayout, QWidget, QGroupBox, QLabel
from PyQt6.QtGui import QTextOption, QIcon
from PyQt6.QtCore import Qt, QSize
from workingDir import _createWorkingDir
from specificationsWindow import _createSpecifications
from versionPickerWindow import _createVersionPicker
from verifyWindow import _createVerify
from downloadMenu import _createDownload
from statusMenu import _createStatusSite
from updateDbWindow import _createUpdateDb
from editorWindow import _createEditor
from genWindow import _createGenerator
__version__ = '1.0.1'

class KoboPatchFanUi(QMainWindow):
  """KoboPatchFan's view (GUI)."""
  def __init__(self):
    """View initializer."""
    super().__init__()

    self.setWindowTitle('KoboPatchFan {}'.format(__version__))
    self.setMinimumSize(QSize(600, 600))

    self.tab_widget = mainTabs(self)
    self.setCentralWidget(self.tab_widget)

    self._createStatusBar()

  def _createStatusBar(self):
      self.statusbar = self.statusBar()

class mainTabs(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    
    self.generalTabLayout = QHBoxLayout()

    # Initialize tab screen
    self.tabs = QTabWidget()
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.tab3 = QWidget()
    self.tab4 = QWidget()

    # Add tabs
    self.tabs.addTab(self.tab1, "(1) Download")
    self.tabs.addTab(self.tab2, "(2) Select patches")
    self.tabs.addTab(self.tab3, "(3) Generate patch")
    self.tabs.addTab(self.tab4, "Settings")

    # Change font size of tabs
    self.tabs.setStyleSheet("QTabBar::tab { height: 64px; }")

    # Create first (main) tab
    self.tab1.layout = QVBoxLayout(self.tab1)
    self.tab1.layout.setSpacing(0)
    self.tab1.setLayout(self.tab1.layout)
    # Create layout for "Left Half" and "Right Half" boxes
    self.left_half = QVBoxLayout()
    self.right_half = QVBoxLayout()
    self.right_half.setSpacing(0)
    self.left_half.setSpacing(0)
    self.left_half_widget = QWidget()
    self.left_half_widget.setLayout(self.left_half)
    self.right_half_widget = QWidget()
    self.right_half_widget.setLayout(self.right_half)
    # Add "Left Half" and "Right Half" boxes to first tab's layout
    self.tab1_hbox = QHBoxLayout()
    self.tab1_hbox.addWidget(self.left_half_widget)
    self.tab1_hbox.addWidget(self.right_half_widget)
    self.tab1.layout.addLayout(self.tab1_hbox)
    # Add "Info" box to first tab's layout
    # Set stretch factor to make "Left Half" and "Right Half" boxes resizable
    self.tab1_hbox.setStretch(0, 1)
    self.tab1_hbox.setStretch(1, 1)

    # Create second (select) tab
    self.tab2.layout = QVBoxLayout(self.tab2)
    self.tab2.setLayout(self.tab2.layout)
    
    # Create third (generate) tab
    self.tab3.layout = QVBoxLayout(self.tab3)
    self.tab3.setLayout(self.tab3.layout)
    # Add Help groupbox to third tab
    help_box3 = QGroupBox()
    self.tab3.layout.addWidget(help_box3)
    # Add Help label to third tab's groupbox
    self.help_label3 = QLabel("Click on <b>'Run'</b> to generate the file '<b>KoboRoot.tgz</b>' that will apply your selected patches to your Kobo. Connect your Kobo, copy the 'KoboRoot.tgz' to the <b>'.kobo'</b> folder, eject and let your Kobo restart.")
    self.help_label3.setWordWrap(True)
    help_box3_layout = QVBoxLayout()
    help_box3_layout.addWidget(self.help_label3)
    help_box3.setLayout(help_box3_layout)

    # Create 4. (settings) tab
    self.tab4.layout = QVBoxLayout(self.tab4)
    self.tab4.layout.setSpacing(0)
    self.tab4.setLayout(self.tab4.layout)
    # Create layout for "Left Half" and "Right Half" boxes
    self.tab4left_half = QVBoxLayout()
    self.tab4right_half = QVBoxLayout()
    self.tab4right_half.setSpacing(0)
    self.tab4left_half.setSpacing(0)
    self.tab4left_half_widget = QWidget()
    self.tab4left_half_widget.setLayout(self.tab4left_half)
    self.tab4right_half_widget = QWidget()
    self.tab4right_half_widget.setLayout(self.tab4right_half)
    # Create layout for "Log" box
    self.log_box = QGroupBox()
    self.log_box_layout = QVBoxLayout()
    self.log_box.setLayout(self.log_box_layout)
    # Add "Left Half" and "Right Half" boxes to first tab's layout
    self.tab4_hbox = QHBoxLayout()
    self.tab4_hbox.addWidget(self.tab4left_half_widget)
    self.tab4_hbox.addWidget(self.tab4right_half_widget)
    self.tab4.layout.addLayout(self.tab4_hbox)
    # Add "Info" box to first tab's layout
    self.tab4.layout.addWidget(self.log_box)
    self.about_label = QLabel()
    self.about_label.setWordWrap(True)
    self.about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.about_label.setText("<h3>About</h3>")
    self.about_label.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    self.about_label.setStyleSheet('background-color: white;border: 2px solid gray;')
    info_box1 = QGroupBox()
    info_label = QTextEdit()
    info_label.setPlainText("KoboPatchFan "+str(__version__)+" by Tommalka\n\nA GUI application written in PyQt6 for downloading, configuring and generating Kobo patches. \n\nKobopatch is an patching system for Kobo eReaders by pgaskin. See https://www.mobileread.com/forums/showthread.php?t=297338 for more infos.\n\nIf you prefer manual downloads, go to https://pgaskin.net/kobopatch-patches/")
    info_label.document().setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignCenter))
    info_label.setReadOnly(True)
    info_box1_layout = QVBoxLayout()
    info_box1_layout.addWidget(self.about_label)
    info_box1_layout.addWidget(info_label)
    info_box1.setLayout(info_box1_layout)
    self.tab4right_half.addWidget(info_box1)
    # Set stretch factor to make "Left Half" and "Right Half" boxes resizable
    self.tab4_hbox.setStretch(0, 1)
    self.tab4_hbox.setStretch(1, 1)

    # Add tabs to widget
    self.generalTabLayout.addWidget(self.tabs)
    self.setLayout(self.generalTabLayout)

    #Create things
    self._createWorkingDir()
    self._createUpdateDb()
    self._createSpecifications()
    self._createVersionPicker()
    self._createVerify()
    self._createDownload()
    self._createStatusSite()
    self._createEditor()
    self._createGenerator()

  def _createWorkingDir(self):
    _createWorkingDir(self)

  def _createUpdateDb(self):
    _createUpdateDb(self)

  def _createSpecifications(self):
    _createSpecifications(self)

  def _createVersionPicker(self):
   _createVersionPicker(self)

  def _createVerify(self):
    _createVerify(self)

  def _createDownload(self):
    _createDownload(self)
  
  def _createStatusSite(self):
     _createStatusSite(self)

  def _createEditor(self):
    _createEditor(self)

  def _createGenerator(self):
    _createGenerator(self)