from PyQt6.QtCore import QThread, QProcess, pyqtSignal, pyqtSlot
from threadManagerClass import ThreadManager

class ProcessThread(QThread):
    finished = pyqtSignal(int)
    outputChanged = pyqtSignal(str)
    errorChanged = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.threadManagerClass = ThreadManager.get_instance()

    def run(self):
        self.threadManagerClass.acquire()
        self.process = QProcess()
        self.process.setProgram(self.command[0])
        self.process.setArguments(self.command[1:])
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.on_ready_read_standard_output)
        self.process.readyReadStandardError.connect(self.on_ready_read_standard_error)
        self.process.finished.connect(self.on_process_finished)
        self.process.closeWriteChannel()
        self.process.start()
        self.process.waitForFinished(-1)

        #while self.process.state() == QProcess.ProcessState.Running:
        #    pass

        self.finished.emit(self.process.exitCode())
        self.threadManagerClass.release()

    @pyqtSlot()
    def on_ready_read_standard_output(self):
        try:
            data1 = self.process.readAllStandardOutput()
            data_str = str(data1)
            data = data1.data().decode().strip()

            if data:
                self.outputChanged.emit(data + '\n')
                if "Waiting 60 seconds because runnning on Windows" in data_str:
                    #self.outputChanged.emit("Going to kill process and quit thread, however koboptch-windows.exe will run for 60 seconds")
                    self.process.kill()
                    self.quit()
        except Exception as e:
            self.outputChanged.emit("Error reading output: "+str(e)+"\n")

    @pyqtSlot()
    def on_ready_read_standard_error(self):
        try:
            data = self.process.readAllStandardError().data().decode().strip()
            if data:
                self.errorChanged.emit(data + '\n')
        except Exception as e:
            self.outputChanged.emit("Error reading output: "+str(e)+"\n")

    @pyqtSlot(int, QProcess.ExitStatus)
    def on_process_finished(self, exitCode, exitStatus):
        pass
       # self.threadManagerClass.release()
        #self.finished.emit(exitCode)
        