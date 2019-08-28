import glob
import os
from collections import deque

import threading
import time


maxQueueSize = 100



class Gallery(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def PrintDequeList(self):
        print(list(self.filelist))

    def GetDequeFileList(self, to_item):
        #cast deque to list before output
        in_filelist = list(self.filelist)
        lenImageList = len(in_filelist)
        return in_filelist[0:min(lenImageList, to_item)]

    def RefreshList(self, path):

        #assume file format:

        #timestampnumber_phoneNumber_photonumber.jpg

        folder_files = sorted(glob.glob(os.path.join(path,'*.*')), key=os.path.getmtime, reverse=True)


        #assume current filelist is sorted since it is deque by uploaded pic

        currentDequeSize = len(self.filelist)

        currentFilesSize = len(folder_files)



        #if deque = folder files by size, assume no change, no need to update_time
        #else, update

        if currentDequeSize != currentFilesSize:
            #someone delete the files in folder, clear() deque
            self.filelist.clear()
            currentDequeSize = len(self.filelist)

            #logic for min, 1. ax deq
            range_size = min(max(currentDequeSize, maxQueueSize),currentFilesSize) - 1

            for i in range(range_size, -1, -1):
                #remove the folder name, and append to deque
                #let UI to build up the <img> full path for both preview and original referencing
                self.filelist.appendleft(folder_files[i].replace(path,''))
                if len(self.filelist) > maxQueueSize:
                    self.filelist.pop()



    def __init__(self, path, interval=10):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.path = path

        self.filelist = deque()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            self.RefreshList(self.path)
            self.PrintDequeList()

            time.sleep(self.interval)



if __name__ == "__main__":
    glly = Gallery('ContestPhotoPreview/')
    time.sleep(30)
    print('Checkpoint')
    time.sleep(15)
    print('Bye')
