import fnmatch
import os


def delete(path,word):

    L = os.listdir(path)

    for filename in L:

        fp = os.path.join(path,filename)

        if os.path.isfile(fp) and word in filename:

           os.remove(os.path.join(path,filename))


