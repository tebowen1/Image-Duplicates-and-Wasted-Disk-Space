"""
Purpose
Recover wasted disk space, by finding duplicate files. Their removal could potentially free a lot of disk space.

Two things:
1. what image has the most duplicates
2. what image takes the most space

    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = ""
__email__ = ""
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare

def search(file_list):
    '''Looking for duplicate files in the provided list of files:
    returns a list of lists, where each list contains files with the same content'''
    lol = []     #empty list of lists
    while 0 < len(file_list):
        dups = [x for x in file_list if compare(file_list[0], x)]       #copy duplicates of first file in list to dups
        file_list = [x for x in file_list if not compare(file_list[0], x)]   #files that don't compare stays in file list
        if 1 < len(dups):
            lol.append(dups)
    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files:
    returns a list of lists, where each list contains files with the same content"""
    file_sizes = list(map(getsize, file_list))
    file_list = list(filter(lambda x: 1 < file_sizes.count(getsize(x)), file_list))
    return(search(file_list))


def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    if 0 < len(lol):
        print("== == Duplicate File Finder Report == ==")
        ll = max(lol, key = len) #gets max of length of list
        ll.sort() #sorts ll
        print(f"The file with the most duplicates is: {ll[0]}")
        print(f"Here are its {len(ll) - 1} copies:")
        for i in range(1, len(ll)):
            print(ll[i])

        ll = max(lol, key=lambda x: len(x) * getsize(x[0]))
        print('\n')
        print(f"The Most Disk space ({getsize(ll[0]) * (len(ll)-1)}) could be recovered, by deleting copies of this file: {ll[0]}")
        print(f"Here are its {len(ll)-1} copies:")
        for i in range(1, len(ll)):
            print(ll[i])
    else:
        print("No duplicates found")

    print('\n')



if __name__ == '__main__':
    path = join(".", "images")

    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now w/ a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
