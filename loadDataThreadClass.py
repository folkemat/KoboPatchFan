from PyQt6.QtCore import QThread, pyqtSignal
import yaml

class LoadDataThread(QThread):
    data_loaded = pyqtSignal(int, str)
    create_patches_components = pyqtSignal(str, bool, str, str, str, int, str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.checkboxes = []

    def run(self):
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
    
    def findMore(self, patch_name, lines):
        #Search for the corresponding code for each patch name
        i = 0
        more_text = ""
        while i < len(lines):
            if patch_name in lines[i]:
                for j in range(i+1, len(lines)): 
                    if lines[j].startswith(' ') or lines[j].startswith('#') or len(lines[j].strip()) == 0: #A new patch block starts without spaces etc.
                        more_text += lines[j]
                    else:
                        break
            i += 1
        return more_text