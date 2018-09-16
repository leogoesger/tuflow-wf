import os
import errno
from shutil import rmtree, copytree

def generate_file_structure():
    name = raw_input("What is the name for files? -> ")

    if os.path.isdir("outputFiles"):
        rmtree('outputFiles') 
    try:
        copytree("template/init", "outputFiles/" + name)
        

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise