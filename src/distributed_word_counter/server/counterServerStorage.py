from os import listdir
from os.path import *
PATH_TO_FILES = "/home/ruanramos/codes/distributed-systems/src/distributed_word_counter/files"
files = {}

if __name__ == "__main__":
    x = listdir(PATH_TO_FILES)    
    
    files = [join(PATH_TO_FILES, f) for f in x if isfile(join(PATH_TO_FILES, f))]
    for f in files:
        with open(f) as bla:
                print(bla.readlines())
    print(files[0])
