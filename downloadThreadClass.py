import requests
import time
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from threadManagerClass import ThreadManager

class DownloadThread(QThread):
    # pyqtSignals for communication with main thread
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    speed = pyqtSignal(str)
    remaining_time = pyqtSignal(str)
    size = pyqtSignal(str)
    filename = pyqtSignal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.stop_flag = False
        self.pause_flag = False
        self.threadManagerClass = ThreadManager.get_instance()

    def run(self):
        self.threadManagerClass.acquire()
        try:
            # Download the file using the requests library
            response = requests.get(self.url, stream=True)

            # Get the original file name from the response headers
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                filename_index = content_disposition.index('filename=')
                if filename_index != -1:
                    filename = content_disposition[filename_index+len('filename='):]
                    # Strip any quotes and spaces from the filename
                    filename = filename.strip('" ')
                else:
                    # If no filename is specified in the header, use the last part of the URL as the filename
                    filename = self.url.split('/')[-1]
            else:
                # If no Content-Disposition header is present, use the last part of the URL as the filename
                filename = self.url.split('/')[-1]

            # Combine the save path and the filename to get the full save path, exception for db
            if "kfw.js" not in self.save_path and "patches.json" not in self.save_path and "kfw_devices.js" not in self.save_path:
                self.save_path = str(Path(self.save_path) / filename)

            # Calculate the total file size
            total_size = int(response.headers.get("Content-Length", 0))
            block_size = 1024
            wrote = 0
            start_time = time.time()
            with open(self.save_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    # Check if the stop flag is set
                    if self.stop_flag: #cancel download
                        raise Exception("Download cancelled")
                    # Check if the pause flag is set
                    while self.pause_flag:
                        time.sleep(1)
                    wrote = wrote + len(data)
                    f.write(data)
                    # Calculate the progress and emit the pyqtSignal if total_size is above a certain threshold
                    if total_size > 0:
                        progress = int(wrote * 100 / total_size)
                        self.progress.emit(progress)
                        # Calculate the speed and emit the pyqtSignal
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 0:
                            speed = wrote / elapsed_time
                            speed_formatted = self.format_speed(speed)
                            self.speed.emit(speed_formatted)
                            # Calculate the remaining time and emit the pyqtSignal
                            remaining_time = (total_size - wrote) / speed
                            self.remaining_time.emit(self.format_time(remaining_time))
                             # Emit the size pyqtSignal
                            self.size.emit(self.format_size(total_size))
                        else:
                            self.speed.emit("0 B/s")
                            self.remaining_time.emit("00:00:00")
                            self.size.emit("")
            # Emit the finished pyqtSignal with the name of the downloaded file
            self.speed.emit("0 B/s - Done!")
            self.remaining_time.emit("00:00:00 - Done!")
            self.size.emit("Done!")
            #print("Finish Download thread released")
            self.threadManagerClass.release()
            self.finished.emit(filename)
        except Exception as e:
            # Emit the error pyqtSignal with the error message
            self.speed.emit("0 B/s")
            self.remaining_time.emit("00:00:00")
            self.size.emit("")
            self.progress.emit(0)
            self.threadManagerClass.release()
            self.error.emit(str(e))

    def stop(self):
        self.stop_flag = True

    def pause(self):
        self.pause_flag = True

    def resume(self):
        self.pause_flag = False

    def format_time(self, time_in_seconds):
        hours, remainder = divmod(time_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    def format_size(self, size_in_bytes):
        if size_in_bytes < 1024:
            return '{} B'.format(size_in_bytes)
        elif size_in_bytes < 1024 * 1024:
            return '{:.2f} KB'.format(size_in_bytes / 1024)
        elif size_in_bytes < 1024 * 1024 * 1024:
            return '{:.2f} MB'.format(size_in_bytes / (1024 * 1024))
        else:
            return '{:.2f} GB'.format(size_in_bytes / (1024 * 1024 * 1024))
    
    def format_speed(self, speed_in_bytes_per_second):
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while speed_in_bytes_per_second >= 1024 and unit_index < len(units) - 1:
            speed_in_bytes_per_second /= 1024
            unit_index += 1
        return '{:.2f} {}'.format(speed_in_bytes_per_second, units[unit_index])