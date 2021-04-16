import os


def get_file_names(path):
    for root, dirs, files in os.walk(path):
        return files


def get_dir_names(path):
    for root, dirs, files in os.walk(path):
        return dirs


def get_sec(time1):
    time1 = str(time1)
    try:
        tmp = time1.split(':')
    except:
        return 0
    if len(tmp) < 3:
        return 0
    return int(tmp[0]) * 3600 + int(tmp[1]) * 60 + int(tmp[2])


path = '../data/k4a-ts/20201106_morning.txt'
fin = open(path, 'r')
fout = open(path[:-4] + '-2.txt', 'w')

for line in fin.readlines():
    ele = line.split()[:3]
    start = float(ele[0]) - 12 * 3600
    end = float(ele[1]) - 12 * 3600
    fout.write('{} {} {}\n'.format(round(start, 3),
                                   round(end, 3),
                                   ele[2]))
