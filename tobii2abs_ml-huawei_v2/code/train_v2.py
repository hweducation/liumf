import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score, roc_auc_score

import pydotplus
import os

os.environ["path"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'


def load_data():
    path = '../data/output_v2.csv'
    fin = open(path, 'r')
    result = []
    for line in fin.readlines():
        elements = line.split(',')[:-1]
        result.append([float(x) for x in elements[1:]])
    return np.array(result)


def preprocess_array(raw_data):
    for i in range(raw_data.shape[0]):
        if raw_data[i][-1] == 1.0 or raw_data[i][-1] == 2.0:
            raw_data[i][-1] = 0
        else:
            raw_data[i][-1] = 1
    # np.random.seed(25)

    abs0, abs1 = raw_data[raw_data[:, -1] == 0, :], raw_data[raw_data[:, -1] == 1, :]
    abs1 = abs1[:abs0.shape[0], :]
    raw_data = np.concatenate((abs0, abs1), axis=0)
    row_rand_array = np.arange(raw_data.shape[0])
    np.random.shuffle(row_rand_array)
    raw_data = raw_data[row_rand_array]
    print(raw_data.shape)
    return raw_data[:, :-1], raw_data[:, -1]


if __name__ == '__main__':
    data = np.load('../data/v2_array_no_zero.npy')
    data[np.isnan(data)] = 0
    X, y = preprocess_array(data)
    offset0, offset1 = int(0.8 * X.shape[0]), int(0.9 * X.shape[0])
    X_train, y_train, X_test, y_test = X[:offset0], y[:offset0], X[offset1:], y[offset1:]
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    prd = clf.predict(X_test)
    print(accuracy_score(y_test, prd))
    print(recall_score(y_test, prd))
    print(f1_score(y_test, prd))
    print(roc_auc_score(y_test, prd))

    exit()
    importance = clf.feature_importances_
    tmp0 = np.argsort(importance)

    fout = open('../data/ranking.csv', 'w')
    fout.write('number of features,acc,recall,f1,roc,\n')
    for i in range(90):
        print(i)
        imp_args = tmp0 > (89 - i)
        tmp = np.argwhere(imp_args).flatten()
        X_train0, X_test0 = X_train[:, tmp], X_test[:, tmp]

        clf = RandomForestClassifier()
        clf.fit(X_train0, y_train)
        prd = clf.predict(X_test0)
        fout.write('{},{},{},{},{},\n'.format(i + 1,
                                              accuracy_score(y_test, prd),
                                              recall_score(y_test, prd),
                                              f1_score(y_test, prd),
                                              roc_auc_score(y_test, prd)))
