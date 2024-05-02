import sys
from cx_Freeze import setup, Executable

upgrade_code = "{C7CB90F8-8360-45C0-9A8B-206CA49DFC8B}"

is_windows = sys.platform.startswith('win')

icon_path = 'kpf.ico'

script_name = "main.py"

exe_name = "KoboPatchFan.exe"
linux_name = "KoboPatchFan"

# Specify the application name and version
APP_NAME = "KoboPatchFan"
APP_VERSION = "1.3.0"


build_exe_options = {
    "packages": ["PyQt6.QtWidgets", "PyQt6.QtCore", "yaml", "chardet"],
    'excludes': ['tkinter'],
    "include_msvcr": True,
    "include_files": [icon_path] if is_windows else []
    }
    
# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

executable = Executable(script=script_name, base=base, target_name=exe_name if is_windows else linux_name, icon=icon_path if is_windows else None)

setup(
    name=APP_NAME,
    version=APP_VERSION,
    url="https://github.com/folkemat/KoboPatchFan",
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