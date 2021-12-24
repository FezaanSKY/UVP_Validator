import os
import hashlib
import sys

def calculate_md5_checksum_filesize(filename):
    # filename = r'C:\Users\fna08\Desktop\PlaygroundProject\Two_Movies.tar_Extracted\5K8554W_TSD.mxf'
    hasher = hashlib.md5()
    with open(filename, 'rb') as open_file:
        content = open_file.read()
        hasher.update(content)
    #Checksum
    checksum = (hasher.hexdigest())
    #Filesize
    filesize = (os.stat(filename).st_size)
    return  str(filesize), checksum


