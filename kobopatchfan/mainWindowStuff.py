# Filename: mainWindowStuff.py

from PyQt6.QtWidgets import  QHBoxLayout, QMainWindow, QTextEdit, QTabWidget, QVBoxLayout, QWidget, QGroupBox, QLabel
from PyQt6.QtGui import QTextOption
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
from savedPatchesWindow import _createSavedPatches
__version__ = '1.2.0'

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
    self.tab5 = QWidget()

    # Add tabs
    self.tabs.addTab(self.tab1, "(1) Download")
    self.tabs.addTab(self.tab2, "(2) Select patches")
    self.tabs.addTab(self.tab3, "(3) Generate patch")
    self.tabs.addTab(self.tab4, "Backup patches")
    self.tabs.addTab(self.tab5, "Settings")

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

    # Create 4. (kobopatch.yaml) tab
    self.tab4.layout = QVBoxLayout(self.tab4)
    self.tab4.setLayout(self.tab4.layout)

    help_box4 = QGroupBox()
    self.tab4.layout.addWidget(help_box4)
    # Add Help label to third tab's groupbox
    self.help_label4 = QLabel("The options here <b>survive</b> downloading new versions, so you don't have to select them again. To <b>add</b> a new option, click on <b>'Backup selection'</b> in tab (2). To <b>use</b> it, select <b>'Use backup patches'</b> in tab (3).")
    self.help_label4.setWordWrap(True)
    help_box4_layout = QVBoxLayout()
    help_box4_layout.addWidget(self.help_label4)
    help_box4.setLayout(help_box4_layout)


    # Create 5. (settings) tab
    self.tab5.layout = QVBoxLayout(self.tab5)
    self.tab5.layout.setSpacing(0)
    self.tab5.setLayout(self.tab5.layout)
    # Create layout for "Left Half" and "Right Half" boxes
    self.tab5left_half = QVBoxLayout()
    self.tab5right_half = QVBoxLayout()
    self.tab5right_half.setSpacing(0)
    self.tab5left_half.setSpacing(0)
    self.tab5left_half_widget = QWidget()
    self.tab5left_half_widget.setLayout(self.tab5left_half)
    self.tab5right_half_widget = QWidget()
    self.tab5right_half_widget.setLayout(self.tab5right_half)
    # Create layout for "Log" box
    self.log_box = QGroupBox()
    self.log_box_layout = QVBoxLayout()
    self.log_box.setLayout(self.log_box_layout)
    # Add "Left Half" and "Right Half" boxes to first tab's layout
    self.tab5_hbox = QHBoxLayout()
    self.tab5_hbox.addWidget(self.tab5left_half_widget)
    self.tab5_hbox.addWidget(self.tab5right_half_widget)
    self.tab5.layout.addLayout(self.tab5_hbox)
    # Add "Info" box to first tab's layout
    self.tab5.layout.addWidget(self.log_box)
    self.about_label = QLabel()
    self.about_label.setWordWrap(True)
    self.about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.about_label.setText("<h3>About</h3>")
    self.about_label.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    self.about_label.setStyleSheet('background-color: white;border: 2px solid gray;')
    info_box1 = QGroupBox()
    info_label = QTextEdit()
    info_label.setPlainText("KoboPatchFan "+str(__version__)+" by Tommalka\n(https://github.com/folkemat/KoboPatchFan)\n\nA GUI application written in PyQt6 for downloading, configuring and generating Kobo patches. \n\nKobopatch is an patching system for Kobo eReaders by pgaskin. See https://www.mobileread.com/forums/showthread.php?t=297338 for more infos.\n\nIf you prefer manual downloads, go to https://pgaskin.net/kobopatch-patches/")
    info_label.document().setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignCenter))
    info_label.setReadOnly(True)
    info_box1_layout = QVBoxLayout()
    info_box1_layout.addWidget(self.about_label)
    info_box1_layout.addWidget(info_label)
    info_box1.setLayout(info_box1_layout)
    self.tab5right_half.addWidget(info_box1)
    # Set stretch factor to make "Left Half" and "Right Half" boxes resizable
    self.tab5_hbox.setStretch(0, 1)
    self.tab5_hbox.setStretch(1, 1)

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
    self._createSavedPatches()

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
  
  def _createSavedPatches(self):
    _createSavedPatches(self)