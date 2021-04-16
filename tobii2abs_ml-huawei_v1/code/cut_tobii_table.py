"""
step 1
cut tobii table, which is based on adjusted_absorbed_states.csv
IN: adjusted_absorbed_states.csv, tobii files
OUT: abs_0.csv abs_1.csv, abs_2.csv, abs_3.csv, abs_4.csv
"""
path_in = '../data/adjusted_absorbed_states.csv'
path1 = 'E:\\data\\第一批26位学生加2-多维数据\\'
path2 = 'E:\\data\\第二批27位学生-多维数据\\'
suffix = '\\Tobii\\Project2 Data Export.csv'


def process_name(name):
    name = name.replace('_', '-')
    return name[:4] + '-' + name[4:6] + '-' + name[6:]


def cut_tobii_table():
    f0 = open('../data/abs_0.csv', 'w')
    f1 = open('../data/abs_1.csv', 'w')
    f2 = open('../data/abs_2.csv', 'w')
    f3 = open('../data/abs_3.csv', 'w')
    f4 = open('../data/abs_4.csv', 'w')
    fin = open(path_in, 'r')
    now_name = ''
    # forget the next line, just use that line to create a var
    f_tobii = open('../data/tmp.txt')
    for line in fin.readlines():
        elements = line.split(',')[:-1]
        if elements[0] == 'name':
            continue
        if now_name != elements[0]:
            print('starting ', elements[0])
            now_name = elements[0]
            f_tobii.close()
            try:
                f_tobii = open(path1 + process_name(now_name) + suffix, 'r')
            except FileNotFoundError:
                f_tobii = open(path2 + process_name(now_name) + suffix, 'r')
            f_tobii.readline()
        label = elements[1]
        start = float(elements[2]) * 1000000
        end = float(elements[3]) * 1000000

        # it is  kind of ugly, but works well
        if label == '0':
            while True:
                tobii_line = f_tobii.readline()
                try:
                    tobii_time = int(tobii_line.split(',', 1)[0])
                except:
                    break
                if start < tobii_time < end:
                    f0.write(tobii_line)
                elif start >= tobii_time:
                    continue
                else:
                    break
            f0.write('\n')
        elif label == '1':
            while True:
                tobii_line = f_tobii.readline()
                try:
                    tobii_time = int(tobii_line.split(',', 1)[0])
                except:
                    break
                if start < tobii_time < end:
                    f1.write(tobii_line)
                elif start >= tobii_time:
                    continue
                else:
                    break
            f1.write('\n')
        elif label == '2':
            while True:
                tobii_line = f_tobii.readline()
                try:
                    tobii_time = int(tobii_line.split(',', 1)[0])
                except:
                    break
                if start < tobii_time < end:
                    f2.write(tobii_line)
                elif start >= tobii_time:
                    continue
                else:
                    break
            f2.write('\n')
        elif label == '3':
            while True:
                tobii_line = f_tobii.readline()
                try:
                    tobii_time = int(tobii_line.split(',', 1)[0])
                except:
                    break
                if start < tobii_time < end:
                    f3.write(tobii_line)
                elif start >= tobii_time:
                    continue
                else:
                    break
            f3.write('\n')
        elif label == '4':
            while True:
                tobii_line = f_tobii.readline()
                try:
                    tobii_time = int(tobii_line.split(',', 1)[0])
                except:
                    break
                if start < tobii_time < end:
                    f4.write(tobii_line)
                elif start >= tobii_time:
                    continue
                else:
                    break
            f4.write('\n')


if __name__ == '__main__':
    cut_tobii_table()
