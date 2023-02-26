import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["PyQt6.QtWidgets", "PyQt6.QtCore", "yaml", "chardet"]}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="KoboPatchFan",
    version="1.0",
    description="My PyQt6 App",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="kpf.ico")],
)