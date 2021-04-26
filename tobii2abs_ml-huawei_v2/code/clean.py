"""
delete the segments which is not 15s
"""
import pandas as pd


def clean(path):
    fin = open(path, 'r')
    lines = fin.readlines()
    fin.close()
    fout = open(path, 'w')
    for line in lines:
        elements = line.split(',')
        start, end = float(elements[2]), float(elements[3])
        if end - start != 15:
            continue
        fout.write(line)


if __name__ == '__main__':
    clean('../data/abs_with_face.csv')
