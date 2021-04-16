"""
step 1
get the time difference to time_diff_k4a-tobii.csv
"""
from tool import *
import os


def get_time_difference():
    path1 = '../data/k4a-ts/'
    path2 = '../data/tobii-ts/'

    names = get_file_names(path1)
    f0 = open('../data/time_diff_k4a-tobii.csv', 'w')
    for name in names:
        # os.rename(path1 + name, path1 + name.replace('-', ''))
        # os.rename(path2 + name, path2 + name.replace('-', ''))
        try:
            f1 = open(path1 + name, 'r')
            f2 = open(path2 + name, 'r')
        except FileNotFoundError:
            continue
        try:
            start1 = float(f1.readline().split()[0])
        except ValueError:
            start1 = float(f1.readline().split()[1])
        try:
            start2 = float(f2.readline().split()[0])
        except ValueError:
            start2 = float(f2.readline().split()[1])
        f0.write(name[:-4] + ',' + str(round(start1 - start2, 3)) + ',\n')
        f1.close()
        f2.close()
    f0.close()


if __name__ == '__main__':
    get_time_difference()
