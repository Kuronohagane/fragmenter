from shutil import copyfile, rmtree
from os import remove, path, makedirs
import random


class Fragmenter:

    diskPath = ""

    def __init__(self, diskPath):
        random.seed()
        self.diskPath = diskPath


    def initFileBranches(self):

        if path.exists(self.diskPath + "branch1"):
            rmtree(self.diskPath + "branch1")
        makedirs(self.diskPath + "branch1")

        if path.exists(self.diskPath + "branch2"):
            rmtree(self.diskPath + "branch2")
        makedirs(self.diskPath + "branch2")


    def fillDriveOnAlternatingFileBranches(self):
        
        fileCounter = 0
        try:
            while True:
                copyfile(self.diskPath + "source" + str(random.randint(1, 4)) + ".txt",
                         self.diskPath + "branch1/data" + str(fileCounter) + ".txt")

                copyfile(self.diskPath + "source" + str(random.randint(1, 4)) + ".txt",
                         self.diskPath + "branch2/data" + str(fileCounter) + ".txt")
                fileCounter += 1
        except OSError as diskFullError:
            if diskFullError.args[0] != 28:
                # if it's not the "disk full" exception (error code 28), send it up
                raise
            else:
                print("Disk has been filled with garbage data")

    def clearFileBranch(self, branchNumber):
        
        if path.exists(self.diskPath + "branch" + str(branchNumber)):
            rmtree(self.diskPath + "branch" + str(branchNumber))
        makedirs(self.diskPath + "branch" + str(branchNumber))
        print("Branch " + str(branchNumber) + " has been deleted")

    def fillFileBranch(self, branchNumber):
        
        fileCounter = 0
        try:
            while True:
                copyfile(self.diskPath + "source" + str(random.randint(1, 4)) + ".txt",
                         self.diskPath + "branch" + str(branchNumber) + "/data" + str(fileCounter) + ".txt")
                fileCounter += 1
                
        except OSError as diskFullError:
            if diskFullError.args[0] != 28:
                # if it's not the "disk full" exception (error code 28), send it up
                raise
            else:
                print("Branch " + str(branchNumber) + " has been filled with garbage data")

    def fragmentDrive(self, numberOfIterations = 1):

        self.initFileBranches()
        self.fillDriveOnAlternatingFileBranches()
        
        currentBranchNumber = 1
        for i in range(1, numberOfIterations + 1):
            print("Entering iteration " + str(i))
            self.clearFileBranch(currentBranchNumber)
            self.fillFileBranch(currentBranchNumber)

            if currentBranchNumber == 1:
                currentBranchNumber = 2
            else:
                currentBranchNumber = 1
        

frag = Fragmenter("D:/")
frag.fragmentDrive()
