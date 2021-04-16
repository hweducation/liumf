import numpy as np


path1 = '../data/k4a-ts/20201126.txt'
path1_out = '../data/k4a-ts/20201126_2.txt'
path2 = '../data/tobii-ts/20201126.txt'
path2_out = '../data/tobii-ts/20201126_2.txt'
time_diff_1_2 = 2720.039


def tmp(path, path_out, time_diff):
    fin = open(path, 'r')
    fout = open(path_out, 'w')
    for line in fin.readlines():
        elem = line.split()
        fout.write(str(round(float(elem[0]) - time_diff, 3)) + ' '
                   + str(round(float(elem[1]) - time_diff, 3)) + ' '
                   + elem[2] + '\n')


if __name__ == '__main__':
    # tmp(path1, path1_out, time_diff_1_2)
    # tmp(path2, path2_out, time_diff_1_2)
    print(np.mean([1, 2, 3]))
    print(np.mean(np.array([1, 2, 3])))
