"""
Step 3
Merge the k4a files divided
In this project, just merge the rows which record the divided files
And adjust the time difference
IN: absorbed_segments_1.csv, absorbed_segments_2.csv
OUT: absorbed_states.csv, adjusted_absorbed_states.csv
"""
out_path = '../data/absorbed_states.csv'
adjusted_out_path = '../data/adjusted_absorbed_states.csv'


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
    fin = open(path, 'r')
    fout = open('../data/absorbed_states.csv', 'w')

    # vars that avoid call the method repeatedly
    now_name = ''
    diff = 0

    for line in fin.readlines():
        elements = line.split(',')[:-1]
        if elements[0][-2] != '_':
            fout.write(line)
            continue
        if elements[0] != now_name:
            now_name = elements[0]
            diff = get_divided_time_diff(now_name)
        fout.write(elements[0][:-2] + ',' + elements[1] + ','
                   + str(round(float(elements[2]) + diff, 3)) + ','
                   + str(round(float(elements[3]) + diff, 3)) + ',\n')


def adjust():
    f_time_diff = open('../data/time_diff_k4a-tobii.csv', 'r')
    time_diff = {}
    for line in f_time_diff.readlines():
        elements = line.split(',')[:-1]
        time_diff[elements[0]] = round(float(elements[1]), 3)

    fin = open(out_path, 'r')
    fout = open(adjusted_out_path, 'w')
    # is_first_line = True
    for line in fin.readlines():
        # if is_first_line:
        #     fout.write(line)
        #     is_first_line = False
        #     continue
        elements = line.split(',')
        if elements[0] == 'name':
            continue
        try:
            fout.write(elements[0] + ','
                       + elements[1] + ','
                       + str(round(float(elements[2]) - time_diff[elements[0]], 3)) + ','
                       + str(round(float(elements[3]) - time_diff[elements[0]], 3)) + ',\n')
        except KeyError:
            print(elements)


if __name__ == '__main__':
    # path1 = '../data/absorbed_segments.csv'
    # merge(path1)
    adjust()
