import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score,\
    f1_score, roc_auc_score, precision_score
from scipy.stats import pearsonr
from scipy.stats import fisher_exact


def load_data():
    path = '../data/abs_with_face.csv'
    fin = open(path, 'r')
    data = []
    for line in fin.readlines():
        elements = line.split(',')[:-1]
        tmp = [int(x) for x in elements[4:]]
        if 1 not in tmp:
            continue
        try:
            ans = int(float(elements[1]))
        except ValueError:
            # print('===', line, '===')
            continue
        if ans == 0:
            continue
        if ans == 1 or ans == 2:
            ans = 0
        else:
            ans = 1
        tmp.append(ans)
        data.append(tmp)
    return np.array(data)


def load_data_for_corr():
    path = '../data/abs_with_face.csv'
    fin = open(path, 'r')
    data = []
    for line in fin.readlines():
        elements = line.split(',')[:-1]
        tmp = [int(x) for x in elements[4:]]
        try:
            ans = int(float(elements[1]))
        except ValueError:
            # print('===', line, '===')
            continue
        if ans == 0:
            continue
        if ans == 3 or ans == 4:
            ans = 0
        else:
            ans = 1
        tmp.append(ans)
        data.append(tmp)
    return np.array(data)


def load_data_with_name():
    path = '../data/abs_with_face.csv'
    fin = open(path, 'r')
    data = []
    for line in fin.readlines():
        elements = line.split(',')[:-1]
        tmp = [elements[0]]
        tmp += [int(x) for x in elements[4:]]
        # if 1 not in tmp:
        #     continue
        # try:
        #     ans = int(float(elements[1]))
        # except ValueError:
        #     # print('===', line, '===')
        #     continue
        # if ans == 0:
        #     continue
        # if ans == 1 or ans == 2:
        #     ans = 0
        # else:
        #     ans = 1
        # tmp.append(ans)
        data.append(tmp)
    return np.array(data)


def face_plot():
    matrix = load_data_with_name()
    print(matrix.shape)
    data_dict = {}
    total_dict = {}
    for i in range(matrix.shape[0]):
        if matrix[i][0] not in total_dict:
            total_dict[matrix[i][0]] = 0
        total_dict[matrix[i][0]] += 1

        for j in range(1, matrix.shape[1]):
            if matrix[i][j] == '1':
                if matrix[i][0] not in data_dict:
                    data_dict[matrix[i][0]] = 0
                data_dict[matrix[i][0]] += 1
                break
    names, nums = [], []
    for key in data_dict.keys():
        names.append(key)
        nums.append(data_dict[key] * 15)

    total = []
    for key in total_dict.keys():
        total.append(total_dict[key] * 15)

    f = open('../data/face_num.csv', 'w')
    f.write('name,num,total,\n')
    for i in range(51):
        f.write('{},{},{},\n'.format(names[i], nums[i], total[i]))

    # abs_list = []
    # plt.title('facial feature')
    # plt.xlabel('NAME')
    # plt.ylabel('time(seconds)')
    # plt.bar(range(len(nums)), total, color='grey')
    # plt.bar(range(len(nums)), nums, tick_label=names, color='g')
    # plt.xticks(rotation=270)
    # plt.show()


def face_correlation():
    matrix = load_data_for_corr()
    print(matrix.shape)
    # corr
    # for i in range(17):
    #     cor, p_value = pearsonr(matrix[:, i].T, matrix[:, 17].T)
    #     print(cor, '  ', p_value)

    total_num = matrix.shape[0]
    for i in range(17):
        print(round(matrix[matrix[:, i] == 1].shape[0] / total_num, 4), end='\t')


def fisher():
    matrix = load_data_for_corr()
    data = [[0] * 4 for x in range(17)]
    for i in range(17):
        for j in range(matrix.shape[0]):
            action = 0 if matrix[j][i] == 1 else 1
            focus = 0 if matrix[j][17] == 0 else 2
            data[i][action + focus] += 1
    print(data[3])
    print(np.array(data[3]).reshape(2, 2))

    f = open('../data/2_2_matrix.csv', 'w')
    for i in range(17):
        f.write('{},,,\n'.format(i + 1))
        f.write(',action,no_action,\n')
        f.write('focus,{},{},\n'.format(data[i][0], data[i][1]))
        f.write('no_focus,{},{},\n'.format(data[i][2], data[i][3]))
    for i in range(17):
        tmp = np.array(data[i]).reshape(2, 2)
        odds, pv = fisher_exact(tmp)
        print(odds, ', ', pv)


def facial_ml():
    matrix = load_data()
    abs0, abs1 = matrix[matrix[:, -1] == 0, :], matrix[matrix[:, -1] == 1, :]
    print(abs0.shape)
    print(abs1.shape)
    row_rand_array = np.arange(abs0.shape[0])
    np.random.shuffle(row_rand_array)
    abs0 = abs0[row_rand_array]
    abs1 = abs1[row_rand_array]
    print(abs0.shape)
    print(abs1.shape)
    matrix = np.concatenate((abs0, abs1), axis=0)
    row_rand_array = np.arange(matrix.shape[0])
    np.random.shuffle(row_rand_array)
    matrix = matrix[row_rand_array]
    x, y = matrix[:, :-1], matrix[:, -1]
    offset = int(0.9 * matrix.shape[0])
    x_train, y_train, x_test, y_test = x[:offset], y[:offset], x[offset:], y[offset:]

    clf = RandomForestClassifier()
    clf.fit(x_train, y_train)
    prd = clf.predict(x_test)
    print(precision_score(y_test, prd))
    print(accuracy_score(y_test, prd))
    print(recall_score(y_test, prd))
    print(f1_score(y_test, prd))
    print(roc_auc_score(y_test, prd))

    print()
    print(clf.feature_importances_)
    importance = clf.feature_importances_
    tmp0 = np.argsort(importance)
    # print(tmp0)
    print(type(tmp0))
    for i in range(len(tmp0)):
        print('facial_feature={}: ranking={}'.format(i + 1, tmp0[i] + 1))


if __name__ == '__main__':
    # face_plot()
    # face_correlation()
    # facial_ml()
    fisher()
