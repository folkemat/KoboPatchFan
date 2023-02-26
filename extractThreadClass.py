#Filename: extractThreadClass.py

from PyQt6.QtCore import QThread, pyqtSignal, QDateTime
from threadManagerClass import ThreadManager
import zipfile
import os

class ExtractThread(QThread):
    progressUpdated = pyqtSignal(int)
    extractionFinished = pyqtSignal(str)
    extractionError = pyqtSignal(str)
    extractionSize = pyqtSignal(str)
    extractionSpeed = pyqtSignal(str)
    extractionRemainingTime = pyqtSignal(str)

    def __init__(self, zip_file_path, extract_path):
        super().__init__()
        self.zip_file_path = zip_file_path
        self.extract_path = extract_path
        self._stop = False
        self.threadManagerClass = ThreadManager.get_instance()

    def run(self):
        self.threadManagerClass.acquire()
        try:
            if not os.path.exists(self.zip_file_path):
                self.extractionError.emit("ZIP file does not exist.")
                self.threadManagerClass.release()
                return
            if not os.path.exists(self.extract_path):
                self.extractionError.emit("Extraction path does not exist.")
                self.threadManagerClass.release()
                return

            # Calculate the size of the ZIP file and emit the extractionSize pyqtSignal
            zip_size = os.path.getsize(self.zip_file_path)
            self.extractionSize.emit(self.format_size(zip_size))

            # Initialize variables for time measurement and speed calculation
            start_time = QDateTime.currentMSecsSinceEpoch()
            processed_size = 0
            last_time = start_time
            last_processed_size = 0

            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                file_count = len(zip_ref.infolist())
                extracted_count = 0
                for member in zip_ref.infolist():
                    if self._stop:
                        break
                    extracted_count += 1
                    progress = int(extracted_count / file_count * 100)
                    self.progressUpdated.emit(progress)

                    # Extract the file and update the processed size
                    if member.filename.endswith('/'):
                        os.makedirs(os.path.join(self.extract_path, member.filename), exist_ok=True)
                        continue
                    zip_ref.extract(member, self.extract_path)
                    processed_size += member.file_size

                    # Calculate the elapsed time and emit the extractionSpeed pyqtSignal
                    current_time = QDateTime.currentMSecsSinceEpoch()
                    elapsed_time = current_time - start_time
                    if elapsed_time > 0:
                        speed = processed_size / elapsed_time * 1000
                        self.extractionSpeed.emit(self.format_speed(speed))

                        # Calculate the remaining time and emit the extractionRemainingTime pyqtSignal
                        if speed > 0:
                            #remaining_size = zip_size - processed_size
                            #remaining_time = remaining_size / speed
                            self.extractionRemainingTime.emit(self.format_remaining_time(elapsed_time, processed_size, zip_size))

                    # Update the last processed size and time
                    if current_time - last_time > 1000:
                        speed = (processed_size - last_processed_size) / (current_time - last_time) * 1000
                        self.extractionSpeed.emit(self.format_speed(speed))
                        last_processed_size = processed_size
                        last_time = current_time

            # Emit the extractionFinished pyqtSignal
            if not self._stop:
                self.extractionRemainingTime.emit("00:00:00 - Done!")
                self.threadManagerClass.release()
                self.extractionFinished.emit("Extraction complete")
            else:
                self.threadManagerClass.release()
                self.extractionFinished.emit("Extraction cancelled")
        except Exception as e:
            self.threadManagerClass.release()
            self.extractionError.emit(str(e))

    def stop(self):
        self._stop = True

    def format_time(self, time_in_seconds):
        hours, remainder = divmod(time_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    
    def format_remaining_time(self, elapsed_time, processed_size, total_size):
        if total_size is None or processed_size >= total_size:
            return '-'

        remaining_size = total_size - processed_size
        remaining_time = remaining_size / (processed_size / elapsed_time)

        return self.format_time(remaining_time / 1000)
    
    def format_speed(self, speed_in_bytes_per_second):
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while speed_in_bytes_per_second >= 1024 and unit_index < len(units) - 1:
            speed_in_bytes_per_second /= 1024
            unit_index += 1
        return '{:.2f} {}'.format(speed_in_bytes_per_second, units[unit_index])

    def format_size(self, size_in_bytes):
        if size_in_bytes < 1024:
            return '{} B'.format(size_in_bytes)
        elif size_in_bytes < 1024 * 1024:
            return '{:.2f} KB'.format(size_in_bytes / 1024)
        else:
            return '{:.2f} MB'.format(size_in_bytes / (1024 * 1024))