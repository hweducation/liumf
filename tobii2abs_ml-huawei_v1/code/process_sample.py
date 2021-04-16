"""
step 2
First of all, do the statistical analysis
Then, clean the data, sample and save them into *.npy file
"""
import numpy as np


def count():
    """
    Count the nums of states in abs_table
    :return: nums of abs_0, 1, 2, 3, 4 in a list
    """
    file_names = ['../data/abs_' + str(x) + '.csv' for x in range(5)]
    nums = {}
    for file_name in file_names:
        print('start {}.'.format(file_name))
        nums[file_name] = 1
        f = open(file_name, 'r')
        for line in f.readlines():
            if line == '\n':
                nums[file_name] += 1
    ans = []
    for file_name in file_names:
        ans.append(nums[file_name])
    return ans


def preprocess_split_data():
    """
    abs_3.csv is too big,
    which make the program runtime more than one day
    that method will tear it into peaces
    """
    path = '../data/abs_3.csv'
    i = 0
    j = 0
    f = open(path, 'r')
    fout = open('../data/abs_3_{}.csv'.format(j), 'w')
    for line in f.readlines():
        fout.write(line)
        if line == '\n':
            i += 1
            if i % 5000 == 0:
                j += 1
                fout.close()
                fout = open('../data/abs_3_{}.csv'.format(j), 'w')


def preprocess(path):
    """
    process raw tobii data to eigenvector and save them into *.npy file
    :param path: abs_*.csv
    :return: None
    """

    def init_dict():
        return {x: [] for x in ['gaze_point', 'gaze_direction', 'pupil_diameter', 'eye_movement']}

    f = open(path, 'r')
    data = init_dict()
    out_array = []
    for line in f.readlines():
        if line == '\n':
            tmp_array = []

            # gaze_point
            gaze_point = np.array(data['gaze_point']).T
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
            def process_dot(dot1, dot2):
                dot0 = []
                for j in range(6):
                    dot0.append(dot1[j] - dot2[j])
                return (pow(dot0[0] ** 2 + dot0[1] ** 2 + dot0[2] ** 2, 0.5)
                        + pow(dot0[3] ** 2 + dot0[4] ** 2 + dot0[5] ** 2, 0.5))

            gaze_direction_delta_lst = []
            if len(data['gaze_direction']) < 2:
                for tmp_i in range(7):
                    tmp_array.append(0)
            else:
                tmp_dot = data['gaze_direction'][0]
                for i in range(1, len(data['gaze_direction'])):
                    now_dot = data['gaze_direction'][i]
                    gaze_direction_delta_lst.append(process_dot(now_dot, tmp_dot))
                    tmp_dot = now_dot
                gaze_direction_delta = np.array(gaze_direction_delta_lst)
                mean = np.mean(gaze_direction_delta)
                tmp_array.append(mean)
                tmp_array.append(np.max(gaze_direction_delta))
                tmp_array.append(np.min(gaze_direction_delta))
                tmp_array.append(np.median(gaze_direction_delta))
                tmp_array.append(np.std(gaze_direction_delta))
                tmp_array.append(np.mean((gaze_direction_delta - mean) ** 3))
                tmp_array.append(np.mean((gaze_direction_delta - mean) ** 4) / pow(np.var(gaze_direction_delta), 2))

            # pupil diameter
            pupil_diameter = np.array(data['pupil_diameter']).T
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
            for i_lst in data['eye_movement']:
                if last_type != i_lst[0]:
                    tmp_dist[i_lst[0]] += i_lst[1]
                    last_type = i_lst[0]

            for i_type in types:
                tmp_array.append(tmp_dist[i_type])
            data = init_dict()
            if np.max(tmp_array[:-4]) != 0:
                out_array.append(tmp_array)
            continue

        elements = line.split(',')

        # gaze point left and right
        try:
            data['gaze_point'].append([float(elements[x]) for x in [26, 27]])
        except ValueError:
            pass
        # gaze direction
        try:
            data['gaze_direction'].append([float(elements[x]) for x in range(32, 38)])
        except ValueError:
            pass
        # pupil diameter
        try:
            if float(elements[38]) >= 2 and float(elements[39]) >= 2:
                data['pupil_diameter'].append([float(elements[x]) for x in [38, 39]])
        except ValueError:
            pass
        # eye_movement
        try:
            data['eye_movement'].append([elements[54], int(elements[55])])
        except ValueError:
            pass

    np.save(path[:-4], out_array)
    f.close()


def sample():
    """
    step 1 merge and count
    balance data and save
    """
    # mind wandering samples
    abs_false = ['abs_1.npy', "abs_2.npy"]
    # absorbed samples
    abs_true = []
    for i in range(7):
        abs_true.append('abs_3_{}.npy'.format(i))
    abs_true.append('abs_4.npy')

    # mind wandering
    abs0 = np.concatenate((np.load('../data/' + abs_false[0]), np.load('../data/' + abs_false[1])), axis=0)
    print('numbers of mind wandering samples', abs0.shape)
    # absorbed
    abs1 = np.load('../data/' + abs_true[0])
    for i in range(1, 8):
        abs1 = np.concatenate((abs1, np.load('../data/' + abs_true[i])), axis=0)
    print('numbers of absorbed samples', abs1.shape)
    np.save('../data/sample_0', abs0)
    row_rand_abs1 = np.arange(abs1.shape[0])
    np.random.shuffle(row_rand_abs1)
    np.save('../data/sample_1', abs1[row_rand_abs1[:abs0.shape[0]]])


def main():
    # print(count())  # 783, 2516, 9846, 30996, 127
    for i in [1, 2, 4]:
        preprocess('../data/abs_{}.csv'.format(i))
    for i in range(7):
        print('start abs_3_{}.csv'.format(str(i)))
        preprocess('../data/abs_3_{}.csv'.format(str(i)))
    preprocess('../data/abs_4.csv')
    # preprocess_split_data()
    sample()  # (8638, 39) (26262, 39)


if __name__ == '__main__':
    main()
