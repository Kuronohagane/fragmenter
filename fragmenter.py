from shutil import copyfile, rmtree
from os import makedirs
import random
from pathlib import Path
import string
import sys


class Fragmenter:
    """
     Class used for fragmenting drives.
     Use by passing drive path to constructor, e.q. ' "D:/" ' along with the smaller and larger source junk data file
     sizes in kilobytes, then call the resulting instance's "fragmentDrive()" method.
    """
    drive_path = Path("")
    smaller_source_data_file_size = 0
    larger_source_data_file_size = 0

    def __init__(self, drive_path, smaller_source_data_file_size, larger_source_data_file_size):
        """
         Initialization. Checking if specified directory exists, and whether the file sizes are correct.
        """
        random.seed()
        if smaller_source_data_file_size < 1 or larger_source_data_file_size < 1:
            raise ValueError("File sizes can't be negative")
        if larger_source_data_file_size <= smaller_source_data_file_size:
            raise ValueError("The third constructor parameter (larger source data file size) must be larger than "
                             "the second constructor parameter (smaller source data file size)")
        self.smaller_source_data_file_size = smaller_source_data_file_size
        self.larger_source_data_file_size = larger_source_data_file_size
        self.drive_path = Path(drive_path)
        if not self.drive_path.exists():
            raise FileNotFoundError("Couldn't find the specified drive.")

    def generate_source_data_files(self):
        random_text = "".join([random.choice(string.ascii_letters) for i in range(1024 * self.smaller_source_data_file_size)])
        with open(Path(self.drive_path, "source_data_smaller.txt"), "w") as smaller_source_data_file:
            smaller_source_data_file.write(random_text)

        random_text = "".join([random.choice(string.ascii_letters) for i in range(1024 * self.larger_source_data_file_size)])
        with open(Path(self.drive_path, "source_data_larger.txt"), "w") as larger_source_data_file:
            larger_source_data_file.write(random_text)

        print("Source junk data files have been generated...")

    def fill_drive_on_alternating_file_branches(self):
        """
         Fills the drive's both file branches with files of different sizes in alternating order, meaning a file is
         written to one branch, then the next one is written to the other, then the first one again and so on.
        """
        file_counter = 0
        try:
            while True:
                smaller_source_file_path = Path(self.drive_path, "source_data_smaller.txt")

                branch1_destination_file_path = Path(self.drive_path, "branch1", "data" + str(file_counter) + ".txt")
                copyfile(smaller_source_file_path, branch1_destination_file_path)

                branch2_destination_file_path = Path(self.drive_path, "branch2", "data" + str(file_counter) + ".txt")
                copyfile(smaller_source_file_path, branch2_destination_file_path)

                file_counter += 1

        except OSError as error:
            if error.args[0] == 28: # disk full error
                print("Drive's file branches have been filled with " + str(file_counter) +
                      " " + str(self.smaller_source_data_file_size) + "kb files of junk data...")
            else:
                raise

    def clear_file_branch(self, branch_number):
        """
         Deletes the contents of the branch of the given number, or makes an empty one if it didn't exist beforehand.
         This can cause an permission error, and sometimes goes through and other times just stops the program.
         Not sure why it happens, but running the script in administrator mode and not having the directory open
         in explorer may or may not help.
        """
        branch_path = Path(self.drive_path, "branch" + str(branch_number))
        if branch_path.exists():
            rmtree(branch_path)
        try:
            makedirs(branch_path)
        except PermissionError:
            print("Permission error, try running the script again. It should work eventually.")

        print("Branch " + str(branch_number) + " has been cleared...")

    def fill_file_branch(self, branch_number):
        """
         Fills the drive on the branch of the given number until it is full.
        """
        file_counter = 0
        try:
            while True:
                larger_source_file_path = Path(self.drive_path, "source_data_larger.txt")
                branch_destination_file_path = Path(self.drive_path, "branch" + str(branch_number), "data" + str(file_counter) + ".txt")

                copyfile(larger_source_file_path, branch_destination_file_path)
                file_counter += 1

        except OSError as error:
            if error.args[0] == 28:  # disk full error
                print("Branch " + str(branch_number) + " has been filled with " + str(file_counter) +
                      " " + str(self.larger_source_data_file_size) + "kb files of junk data...")
            else:
                raise

    def fragment_drive(self):
        """
         Fragments a drive of the path passed in the class constructor by filling it with files of the smaller size,
         then deleting every other file, and filling the created holes in drive space with larger files which don't
         fit, causing the new files to be split across these free spaces between the original files. Then, it repeats
         this process for the other branch.
        """
        print("Commencing fragmentation.")

        self.clear_file_branch(1)
        self.clear_file_branch(2)
        self.generate_source_data_files()
        self.fill_drive_on_alternating_file_branches()

        self.clear_file_branch(1)
        self.fill_file_branch(1)
        self.clear_file_branch(2)
        self.fill_file_branch(2)

        print("Fragmentation finished successfully.")
        

# ------------------USAGE--------------------

# Drive path, smaller file in kilobytes, larger file in kilobytes.

# Fragmenter("D:", 600, 1800).fragment_drive()

try:
    Fragmenter(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).fragment_drive()
except IndexError:
    print("Parameters: drive path, smaller junk file size and larger junk file size, "
          "e.q. 'python fragmenter.py D:/ 600 1200'")

