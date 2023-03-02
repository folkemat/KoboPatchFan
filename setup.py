import sys
from cx_Freeze import setup, Executable
import uuid

upgrade_code = '{' + str(uuid.uuid4()).upper() + '}'

is_windows = sys.platform.startswith('win')

icon_path = 'kpf.ico'

script_name = "main.py"

exe_name = "KoboPatchFan.exe"
linux_name = "KoboPatchFan"

# Specify the application name and version
APP_NAME = "KoboPatchFan"
APP_VERSION = "1.0.1"


build_exe_options = {
    "packages": ["PyQt6.QtWidgets", "PyQt6.QtCore", "yaml", "chardet"],
    'excludes': ['tkinter'],
    "include_files": [icon_path] if is_windows else []
    }
    
# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

executable = Executable(script=script_name, base=base, target_name=exe_name if is_windows else linux_name, icon=icon_path if is_windows else None)

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description="KoboPatchFan, GUI application for Kobopatch",
    options={
        "build_exe": build_exe_options,  # merge the build_exe_options dictionary here
        "bdist_msi": {
            "initial_target_dir": r"[ProgramFilesFolder]\KoboPatchFan",
            "add_to_path": True,
            "all_users": True,
            "upgrade_code": upgrade_code,  # GUID to upgrade old installations
            'data': {
            'Shortcut': [
                ('DesktopShortcut', 'DesktopFolder', APP_NAME, 'TARGETDIR', '[TARGETDIR]KoboPatchFan.exe', None, None, None, None, None, None, 'TARGETDIR'),
                ('StartMenuShortcut', 'ProgramMenuFolder', APP_NAME, 'TARGETDIR', '[TARGETDIR]KoboPatchFan.exe', None, None, None, None, None, None, 'TARGETDIR')
                ],
            }
        }
    },
    executables=[executable],
)