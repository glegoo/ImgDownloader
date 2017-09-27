import threading

class myThread (threading.Thread):   
    def __init__(self, dlFunc, images, folder):
        threading.Thread.__init__(self)
        self.dlFunc = dlFunc
        self.images = images
        self.folder = folder

    def run(self):
        self.dlFunc(self.images, self.folder)