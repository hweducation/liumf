import pandas as pd

out_path = '../data/face_states.csv'
adjusted_out_path = '../data/adjusted_face_states.csv'


def get_divided_time_diff(name):
    name0 = name[:-2]
    try:
        f1 = open('../data/k4a-ts/' + name0 + '.txt', 'r')
        f2 = open('../data/k4a-ts/' + name + '.txt', 'r')
    except FileNotFoundError:
        return 0
    try:
        start1 = float(f1.readline().split()[0])
    except ValueError:
        start1 = float(f1.readline().split()[1])
    try:
        start2 = float(f2.readline().split()[0])
    except ValueError:
        start2 = float(f2.readline().split()[1])
    return round(start1 - start2, 3)


def merge(path):
    # fin = open(path, 'r')
    fin = pd.read_csv(path, encoding='gbk')
    fout = open(out_path, 'w')

    # vars that avoid call the method repeatedly
    now_name = ''
    diff = 0

    for i in range(fin.shape[0]):
        elements = fin.values[i]
        if elements[0][-2] != '_':
            fout.write('{},"{}",{},{},\n'.format(elements[0], elements[1], elements[2], elements[3]))
            continue
        if elements[0] != now_name:
            now_name = elements[0]
            # print(now_name)
            diff = get_divided_time_diff(now_name)
        fout.write('{},"{}",{},{},\n'.format(elements[0][:-2],
                                             elements[1],
                                             round(float(elements[2]) + diff, 3),
                                             round(float(elements[3]) + diff, 3)))


def adjust():
    f_time_diff = open('../data/time_diff_k4a-tobii.csv', 'r')
    time_diff = {}
    for line in f_time_diff.readlines():
        elements = line.split(',')[:-1]
        time_diff[elements[0]] = round(float(elements[1]), 3)

    # fin = open(out_path, 'r')
    fin = pd.read_csv(out_path, encoding='gbk')
    fout = open(adjusted_out_path, 'w')

    for i in range(fin.shape[0]):
        elements = fin.values[i]
        try:
            fout.write('{},"{}",{},{},\n'.format(elements[0],
                                                 elements[1],
                                                 round(float(elements[2]) - time_diff[elements[0]], 3),
                                                 round(float(elements[3]) - time_diff[elements[0]], 3)))
        except KeyError:
            # print(elements)
            pass


if __name__ == '__main__':
    path1 = '../data/face_segments.csv'
    merge(path1)
    adjust()
