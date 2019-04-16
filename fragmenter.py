from shutil import copyfile, rmtree
from os import path, makedirs
import random


class Fragmenter:
    """
     Class used for fragmenting drives.
     Use by passing drive path to constructor, e.q. "D:/", then call the instance's "fragmentDrive()" method.
    """
    drive_path = ""

    def __init__(self, drive_path):
        random.seed()
        self.drive_path = drive_path

    def init_file_branches(self):
        """
         Creates 2 "branch" folders which are used to store files written to the drive in alternating order.
         (or clears them if they already exist)
         One branch is supposed to store the odd-written files, and the other stores the even-written files.
        """
        if path.exists(self.drive_path + "branch1"):
            rmtree(self.drive_path + "branch1")
        makedirs(self.drive_path + "branch1")

        if path.exists(self.drive_path + "branch2"):
            rmtree(self.drive_path + "branch2")
        makedirs(self.drive_path + "branch2")

    def fill_drive_on_alternating_file_branches(self):
        """
         Fills the drive's both file branches with files of random sizes in alternating order, meaning a file is written
         to one branch, then the next one is written to the other, then the first one again and so on.
        """
        file_counter = 0
        try:
            while True:
                copyfile(self.drive_path + "source" + str(random.randint(1, 4)) + ".txt",
                         self.drive_path + "branch1/data" + str(file_counter) + ".txt")

                copyfile(self.drive_path + "source" + str(random.randint(1, 4)) + ".txt",
                         self.drive_path + "branch2/data" + str(file_counter) + ".txt")
                file_counter += 1

        except OSError as error:
            if error.args[0] == 28: # disk full error
                print("Disk has been filled with garbage data")
            else:
                raise

    def clear_file_branch(self, branch_number):
        """
         Deletes the contents of the branch of the given number.
        """
        if path.exists(self.drive_path + "branch" + str(branch_number)):
            rmtree(self.drive_path + "branch" + str(branch_number))
        makedirs(self.drive_path + "branch" + str(branch_number))
        print("Branch " + str(branch_number) + " has been deleted")

    def fill_file_branch(self, branch_number):
        """
         Fills the drive on the branch of the given number until it is full.
        """
        file_counter = 0
        try:
            while True:
                copyfile(self.drive_path + "source" + str(random.randint(1, 4)) + ".txt",
                         self.drive_path + "branch" + str(branch_number) + "/data" + str(file_counter) + ".txt")
                file_counter += 1

        except OSError as error:
            if error.args[0] == 28:  # disk full error
                print("Branch " + str(branch_number) + " has been filled with garbage data")
            else:
                raise

    def fragment_drive(self, number_of_iterations=1):
        """
         Fragments a drive of the path passed in the class constructor by filling it with files of various sizes,
         then deleting every other file, and filling the created holes in drive space with more files which don't
         perfectly fit, causing the new files to be split across these free spaces between the original files.
         Such an iteration can be done several times to further increase the severity of fragmentation, but there are
         diminishing returns.
        """
        print("Commencing fragmentation.")
        self.init_file_branches()
        self.fill_drive_on_alternating_file_branches()

        current_branch_number = 1
        for i in range(1, number_of_iterations + 1):
            print("Entering fragmentation iteration " + str(i) + ":")
            self.clear_file_branch(current_branch_number)
            self.fill_file_branch(current_branch_number)

            if current_branch_number == 1:
                current_branch_number = 2
            else:
                current_branch_number = 1

        print("Fragmentation finished.")
        

frag = Fragmenter("D:/")
frag.fragment_drive()
