import numpy as np
import pandas as pd


def process_name(name):
    name = name.replace('_', '-')
    return name[:4] + '-' + name[4:6] + '-' + name[6:]


def preprocess_v2():
    def init_dict():
        return {x: [] for x in ['gaze_point', 'gaze_direction', 'pupil_diameter', 'eye_movement']}

    path1 = 'F:\\data\\第一批26位学生加2-多维数据\\'
    path2 = 'F:\\data\\第二批27位学生-多维数据\\'
    suffix = '\\Tobii\\Project2 Data Export.csv'
    out_path = '../data/output_v2.csv'
    path_abs_face = '../data/abs_with_face.csv'
    data = pd.read_csv(path_abs_face, encoding='gbk')
    fout = open(out_path, 'w')
    now_name = ''
    f_tobii = open('../data/tmp.txt')
    for i_data in range(data.shape[0]):
        valid_data = init_dict()
        tmp_array = []

        if now_name != data.values[i_data][0]:
            now_name = data.values[i_data][0]
            f_tobii.close()
            print('starting ', now_name)
            try:
                f_tobii = open(path1 + process_name(now_name) + suffix, 'r')
            except FileNotFoundError:
                f_tobii = open(path2 + process_name(now_name) + suffix, 'r')
            f_tobii.readline()
        start, end = float(data.values[i_data][2]) * 1e6, float(data.values[i_data][3]) * 1e6
        while True:
            tobii_line = f_tobii.readline()
            try:
                tobii_time = int(tobii_line.split(',', 1)[0])
            except ValueError:
                break
            elements = tobii_line.split(',')
            if start < tobii_time < end:
                # gaze point left and right
                try:
                    valid_data['gaze_point'].append([float(elements[x]) for x in [26, 27]])
                except ValueError:
                    pass
                # gaze direction
                try:
                    valid_data['gaze_direction'].append([float(elements[x]) for x in range(32, 38)])
                except ValueError:
                    pass
                # pupil diameter
                try:
                    if float(elements[38]) >= 2 and float(elements[39]) >= 2:
                        valid_data['pupil_diameter'].append([float(elements[x]) for x in [38, 39]])
                except ValueError:
                    pass
                # eye_movement
                try:
                    valid_data['eye_movement'].append([elements[54], int(elements[55])])
                except ValueError:
                    pass
            elif tobii_time >= end:
                break
        # gaze_point
        gaze_point = np.array(valid_data['gaze_point']).T
        if len(gaze_point) == 0:
            for tmp_i in range(14):
                tmp_array.append(0)
        else:
            for i in range(2):
                if len(gaze_point[i]) == 0:
                    for tmp_i in range(7):
                        tmp_array.append(0)
                else:
                    mean = np.mean(gaze_point[i])
                    tmp_array.append(mean)
                    tmp_array.append(np.max(gaze_point[i]))
                    tmp_array.append(np.min(gaze_point[i]))
                    tmp_array.append(np.median(gaze_point[i]))
                    tmp_array.append(np.std(gaze_point[i]))
                    tmp_array.append(np.mean((gaze_point[i] - mean) ** 3))
                    tmp_array.append(np.mean((gaze_point[i] - mean) ** 4) / pow(np.var(gaze_point[i]), 2))

        # gaze_direction
        gaze_direction = np.array(valid_data['gaze_direction']).T
        if len(gaze_direction) == 0:
            for tmp_i in range(6 * 7):
                tmp_array.append(0)
        else:
            for i in range(6):
                if len(gaze_direction[i]) == 0:
                    for tmp_i in range(7):
                        tmp_array.append(0)
                else:
                    mean = np.mean(gaze_direction[i])
                    tmp_array.append(mean)
                    tmp_array.append(np.max(gaze_direction[i]))
                    tmp_array.append(np.min(gaze_direction[i]))
                    tmp_array.append(np.median(gaze_direction[i]))
                    tmp_array.append(np.std(gaze_direction[i]))
                    tmp_array.append(np.mean((gaze_direction[i] - mean) ** 3))
                    tmp_array.append(np.mean((gaze_direction[i] - mean) ** 4) / pow(np.var(gaze_direction[i]), 2))

        # pupil diameter
        pupil_diameter = np.array(valid_data['pupil_diameter']).T
        if len(pupil_diameter) == 0:
            for tmp_i in range(14):
                tmp_array.append(0)
        else:
            for i in range(2):
                if len(pupil_diameter[i]) == 0:
                    for tmp_i in range(7):
                        tmp_array.append(0)
                else:
                    mean = np.mean(pupil_diameter[i])
                    tmp_array.append(mean)
                    tmp_array.append(np.max(pupil_diameter[i]))
                    tmp_array.append(np.min(pupil_diameter[i]))
                    tmp_array.append(np.median(pupil_diameter[i]))
                    tmp_array.append(np.std(pupil_diameter[i]))
                    tmp_array.append(np.mean((pupil_diameter[i] - mean) ** 3))
                    tmp_array.append(np.mean((pupil_diameter[i] - mean) ** 4) / pow(np.var(pupil_diameter[i]), 2))

        # eye_movement
        last_type = ''
        types = ['Fixation', 'Saccade', 'Unclassified', 'EyesNotFound']
        tmp_dist = {x: 0 for x in types}
        for i_lst in valid_data['eye_movement']:
            if last_type != i_lst[0]:
                tmp_dist[i_lst[0]] += i_lst[1]
                last_type = i_lst[0]
        for i_type in types:
            tmp_array.append(tmp_dist[i_type])

        fout.write('{},{},{},{},\n'.format(data.values[i_data][0],
                                           ','.join([str(x) for x in data.values[i_data][4:21]]),
                                           ','.join([str(x) for x in tmp_array]),
                                           data.values[i_data][1]))


if __name__ == '__main__':
    preprocess_v2()
