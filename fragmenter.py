from shutil import copyfile, rmtree
from os import makedirs
import random
from pathlib import Path


class Fragmenter:
    """
     Class used for fragmenting drives.
     Use by passing drive path to constructor, e.q. ' "D:/" ', then call the resulting instance's "fragmentDrive()"
     method. It requires garbage data text files of slightly different sizes (not multiples) called "source1.txt" and
     "source2.txt", etc, stored at the specified drive path. These will be copied to fragment the drive.
     Change the "source_file_max_number" to utilize more or less files (make sure to put them in the directory).
    """
    drive_path = Path("")
    source_file_max_number = 3

    def __init__(self, drive_path):
        """
         Initialization. Checking if specified directory exists and has the source garbage data files required.
        """
        random.seed()
        self.drive_path = Path(drive_path)
        if self.drive_path.exists():
            for i in range(1, self.source_file_max_number + 1):
                if not (Path(self.drive_path, "source" + str(i) + ".txt")).exists():
                    raise FileNotFoundError("Couldn't find the source" + str(i) + ".txt file.")
        else:
            raise FileNotFoundError("Couldn't find the specified drive.")

    def init_file_branches(self):
        """
         Creates 2 "branch" folders which are used to store files written to the drive in alternating order.
         (or clears them if they already exist)
        """
        branch1_path = Path(self.drive_path, "branch1")
        if branch1_path.exists():
            rmtree(branch1_path)
        makedirs(branch1_path)

        branch2_path = Path(self.drive_path, "branch2")
        if branch2_path.exists():
            rmtree(branch2_path)
        makedirs(branch2_path)

    def fill_drive_on_alternating_file_branches(self):
        """
         Fills the drive's both file branches with files of different sizes in alternating order, meaning a file is
         written to one branch, then the next one is written to the other, then the first one again and so on.
        """
        file_counter = 0
        try:
            while True:
                random_source_file_1_path = Path(self.drive_path, "source" + str(random.randint(1, self.source_file_max_number)) + ".txt")
                branch1_destination_file_path = Path(self.drive_path, "branch1", "data" + str(file_counter) + ".txt")

                random_source_file_2_path = Path(self.drive_path, "source" + str(random.randint(1, self.source_file_max_number)) + ".txt")
                branch2_destination_file_path = Path(self.drive_path, "branch2", "data" + str(file_counter) + ".txt")
                
                copyfile(random_source_file_1_path, branch1_destination_file_path)
                copyfile(random_source_file_2_path, branch2_destination_file_path)
                file_counter += 1

        except OSError as error:
            if error.args[0] == 28: # disk full error
                print("Drive's file branches have been filled with " + str(file_counter) + " files of garbage data")
            else:
                raise

    def clear_file_branch(self, branch_number):
        """
         Deletes the contents of the branch of the given number.
        """
        branch_path = Path(self.drive_path, "branch" + str(branch_number))
        if branch_path.exists():
            rmtree(branch_path)
        makedirs(branch_path)
        print("Branch " + str(branch_number) + " has been cleared")

    def fill_file_branch(self, branch_number):
        """
         Fills the drive on the branch of the given number until it is full.
        """
        file_counter = 0
        try:
            while True:
                random_source_file_path = Path(self.drive_path, "source" + str(random.randint(1, self.source_file_max_number)) + ".txt")
                branch_destination_file_path = Path(self.drive_path, "branch" + str(branch_number), "data" + str(file_counter) + ".txt")

                copyfile(random_source_file_path, branch_destination_file_path)
                file_counter += 1

        except OSError as error:
            if error.args[0] == 28:  # disk full error
                print("Branch " + str(branch_number) + " has been filled with " + str(file_counter) + " files of garbage data")
            else:
                raise

    def fragment_drive(self, number_of_iterations=1):
        """
         Fragments a drive of the path passed in the class constructor by filling it with files of different sizes,
         then deleting every other file, and filling the created holes in drive space with more files which often don't
         perfectly fit, causing the new files to be split across these free spaces between the original files.
         Then, it repeats this for the other branch. Such an iteration can be done several times to further increase
         the severity of fragmentation, but there are diminishing returns.
        """
        print("Commencing fragmentation.")
        self.init_file_branches()
        self.fill_drive_on_alternating_file_branches()

        for i in range(1, number_of_iterations + 1):
            print("Entering fragmentation iteration " + str(i) + ":")
            self.clear_file_branch(1)
            self.fill_file_branch(1)
            self.clear_file_branch(2)
            self.fill_file_branch(2)

        print("Fragmentation finished.")
        

# ------------------USAGE--------------------

Fragmenter("D:").fragment_drive()


