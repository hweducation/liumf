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
