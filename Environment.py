import tarfile
import os
import common


class Environment:
    filelocation = ""
    working_environment = ""

    def __init__(self, filelocation):
        # file inputted by user and storing filelocation as a class variable
        self.filelocation = filelocation

    def getFilePath(self, filename):
        return self.working_environment + filename

    # after filelocation passed in as string (instantiation (innit function) ) it invokes 'new directory' function - it returns filelocation as a string.
    def new_directory(self ) -> str:
        return self.__untar__()

## once filelocation is saved as a string. In new_directory we call the untar (private function below) which untars the file and saves the string to the working environment.

    # private function
    def __untar__(self):
        # declare filename
        filename = os.path.basename(self.filelocation)
        # open file in write mode
        file_obj = tarfile.open(str(self.filelocation), "r")
        # get the names of files in tar file
        namelist = file_obj.getnames()
        # print the filenames
        inside_tar = ""
        message = ("The following files are being extracted:")
        for name in namelist:
            inside_tar += common.makeline(name)
        # extract all files
        file = file_obj.extractall(f"{filename}_Extracted")
        # close file
        file_obj.close()
        self.working_environment = f"{filename}_Extracted/"
        # self.working_environment = self.filelocation.replace(".uvp", ".uvp_Extracted/")
        # self.working_environment = self.working_environment.replace("/TestPackage", "")
        return message + "\n" + inside_tar


