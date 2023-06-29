# KoboPatchFan
A GUI application written in PyQt6 to download, configure and generate Kobo patches.
More info in the forum post on Mobileread: https://www.mobileread.com/forums/showthread.php?t=352447

How does it work?
The application connects to https://github.com/repos/pgaskin/kobopatch-patches/releases/latest to get a list with all current patches and to https://pgaskin.net/KoboStuff/kfw.db.js to get a list of all firmware download links. Based on this, the application checks whether a patch is available for the selected firmware. If this is the case, the corresponding patch file is downloaded from the GitHub release and the firmware from the pages specified in kfw.db.js.
With the help of PyYaml, the .yaml files are searched for the patch options. 
On Linux, the .sh file included in the patch is used to generate the RootKobo.tgz, on Windows the .bat file is executed.

How to build?
To build KoboPatchFan yourself, you need to have Python3, PyQt6 and Yaml installed. 
I used cx_Freeze to create executables (see setup.py).