from PyQt6.QtCore import QMutex

class ThreadManager:
    instance = None

    @staticmethod
    def get_instance():
        if not ThreadManager.instance:
            ThreadManager.instance = ThreadManager()
        return ThreadManager.instance

    def __init__(self):
        self.mutex = QMutex()

    def acquire(self):
        self.mutex.lock()

    def release(self):
        self.mutex.unlock()