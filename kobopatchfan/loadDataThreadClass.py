from PyQt6.QtCore import QThread, pyqtSignal
from configSettingsClass import configSettings
import yaml
import os

class LoadDataThread(QThread):
    data_loaded = pyqtSignal(int, str)
    create_patches_components = pyqtSignal(str, bool, str, str, str, int, str)

    patches_in_kobopatchyaml = pyqtSignal(str, str, bool)
    finish_patches_in_kobopatchyaml = pyqtSignal(int, str)
    finish_all_patches = pyqtSignal(list)

    def __init__(self, file_path, mode, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.mode = mode

    def run(self):        
        ##load 1 patch file##
        if self.mode == 0:
            with open(self.file_path, encoding='utf-8') as file:
                lines = file.readlines()
                data = yaml.safe_load(''.join(lines))
            all_patches = []
            for patch_name, patch_data in data.items():
                description = next((p.get("Description") for p in patch_data if "Description" in p), "No description!")
                enabled = next((p.get("Enabled") for p in patch_data if "Enabled" in p), False)
                patchGroup = next((p.get("PatchGroup") for p in patch_data if "PatchGroup" in p), "None")
                all_text = self.findMore(patch_name, lines)
                all_patches.append([patch_name, enabled, description, patchGroup, all_text])

            numberOfPatch = 0
            for patch in all_patches:
                numberOfPatch = numberOfPatch+1
                checkbox_name = patch[0]
                checkbox_state = patch[1]
                desc_text = patch[2]
                patch_group_text = patch[3]
                more_text = patch[4]
                #create checkbox - calculate self.checkboxes
                self.create_patches_components.emit(checkbox_name, checkbox_state, desc_text, more_text, patch_group_text, numberOfPatch, self.file_path)
            self.data_loaded.emit(numberOfPatch, self.file_path)

        ##load kobopatch.yaml##
        elif self.mode == 1:
            with open(self.file_path, encoding='utf-8') as file:
                lines = file.readlines()
                data = yaml.safe_load(''.join(lines))
            i = 0
            try:
                overrides = data.get('overrides')
                for file_name in overrides:
                    options = overrides.get(file_name)
                    if options:
                        for option in options:
                            state = options.get(option)
                            i = i+1
                            #print(str(i)+": "+file_name+": "+str(option)+" --> "+str(state)+"\n\n")
                            self.patches_in_kobopatchyaml.emit(file_name, option, state)
            except Exception as e:
                configSettings.log(self, "Error kobopatch.yaml: "+str(e))
            self.finish_patches_in_kobopatchyaml.emit(i, self.file_path)

        #get patches of all files##
        elif self.mode == 2: 
            homePath = self.file_path #this is dirty
            src_path = os.path.join(homePath, "src")
            
            file_paths = [
                os.path.join(src_path, "nickel.yaml"),
                os.path.join(src_path, "libnickel.so.1.0.0.yaml"),
                os.path.join(src_path, "librmsdk.so.1.0.0.yaml"),
                os.path.join(src_path, "libadobe.so.yaml")
            ]
            
            all_data = {}
            try:
                for file_path in file_paths:
                    with open(file_path, encoding='utf-8') as file:
                        lines = file.readlines()
                    data = yaml.safe_load(''.join(lines))
                    all_data[file_path] = data
            except Exception as e:
                configSettings.log(self, "Error: Could not open .yaml file: "+str(e))
            
            all_patches = []
            for file_path, data in all_data.items():
                for patch_name, patch_data in data.items():
                    enabled = next((p.get("Enabled") for p in patch_data if "Enabled" in p), False)
                    filename = os.path.basename(file_path)
                    all_patches.append([patch_name, enabled, filename])

            self.finish_all_patches.emit(all_patches)

    def findMore(self, patch_name, lines):
        #Search for the corresponding code for each patch name
        i = 0
        more_text = ""
        while i < len(lines):
            if (patch_name in lines[i]) and not (lines[i].startswith('#') or lines[i].startswith(' ')): #check if patch-name is not a comment
                for j in range(i+1, len(lines)): 
                    if lines[j].startswith(' ') or lines[j].startswith('#') or len(lines[j].strip()) == 0: #A new patch block starts without spaces etc.
                        more_text += lines[j]
                    else:
                        break
            i += 1
        return more_text