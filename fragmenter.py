from shutil import copyfile, rmtree
from os import remove, path, makedirs
import random

diskPath = "D:/"
numberOfIterations = 3


class Fragmenter:

    diskPath = ""
    numberOfIterations = 1
    fileCounter = 0
    currentBranch = 1
    
    def __init__(self, diskPath, numberOfIterations = 1):
        random.seed()
        self.diskPath = diskPath
        self.numberOfIterations = numberOfIterations


    def initBranches(self):

        if path.exists(self.diskPath + "branch1"):
            rmtree(self.diskPath + "branch1")
        makedirs(self.diskPath + "branch1")

        if path.exists(self.diskPath + "branch2"):
            rmtree(self.diskPath + "branch2")
        makedirs(self.diskPath + "branch2")


    def populateDriveWithFiles(self):

        # populate drive with garbage files of random sizes in alternating "branches" (folders) until it's full
        try:
            while True:
                copyfile(self.diskPath + "source" + str(random.randint(1, 4)) + ".txt",
                         self.diskPath + "branch1/data" + str(self.fileCounter) + ".txt")

                copyfile(self.diskPath + "source" + str(random.randint(1, 4)) + ".txt",
                         self.diskPath + "branch2/data" + str(self.fileCounter) + ".txt")
                self.fileCounter += 1
        except OSError as e:
            if e.args[0] != 28:
                # if it's not the "disk full" exception (error code 28), send it up
                raise
            else:
                print("Disk has been populated with garbage data")

    def fragmentPopulatedDrive(self):

        for iterationCounter in range(1, self.numberOfIterations + 1):
            # delete currently considered branch (every second file)
            print("Entering iteration " + str(iterationCounter))
            while self.fileCounter > 0:
                try:
                    remove(self.diskPath + "branch" + str(self.currentBranch) + "/data" + str(self.fileCounter) + ".txt")
                except FileNotFoundError:
                    pass
                self.fileCounter -= 1
            print("Branch " + str(self.currentBranch) + " has been deleted")

            # repopulate the deleted branch with files of different random sizes
            try:
                while True:
                    copyfile(self.diskPath + "source" + str(random.randint(1, 4)) + ".txt",
                             self.diskPath + "branch" + str(self.currentBranch) + "/data" + str(self.fileCounter) + ".txt")
                    self.fileCounter += 1
            except:
                print("Branch " + str(self.currentBranch) + " has been repopulated" )

            # change the current branch to the other one
            if self.currentBranch == 1:
                self.currentBranch = 2
            else:
                self.currentBranch = 1


frag = Fragmenter(diskPath)
frag.initBranches()
frag.fragmentDisk()

