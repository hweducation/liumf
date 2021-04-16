"""
step 6
box/bean plot
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def get_pupil_size(path):
    x, tmp_x = [], []
    f = open(path, 'r')
    for line in f.readlines():
        if line == '\n':
            if np.mean(tmp_x) != 0:
                x.append(np.mean(tmp_x))
            tmp_x.clear()
            continue
        elements = line.split(',')[:-1]
        if elements[38] != '' and elements[39] != '':
            try:
                tmp_x.append((float(elements[38]) + float(elements[39])) / 2.0)
            except ValueError:
                continue
        elif elements[38] != '':
            try:
                tmp_x.append(float(elements[38]))
            except ValueError:
                continue
        elif elements[39] != '':
            try:
                tmp_x.append(float(elements[39]))
            except ValueError:
                continue

    f.close()
    return np.array(x)


def save_data():
    path0 = '../data/abs_0.csv'
    path1 = '../data/abs_1.csv'
    x0 = get_pupil_size(path0)
    np.save('../data/x0_pupil.npy', x0)
    x1 = get_pupil_size(path1)
    np.save('../data/x1_pupil.npy', x1)


def box_plot():
    x0 = np.load('../data/x0_pupil.npy')
    x1 = np.load('../data/x1_pupil.npy')
    x0 = x0[np.logical_not(np.isnan(x0))]
    x1 = x1[np.logical_not(np.isnan(x1))]
    x = [x0, x1]
    plt.boxplot(x)
    plt.xticks(range(0, 3), labels=['', 'mind wandering', 'attended'])
    plt.ylabel('Pupil Size')
    plt.title('Pupil size of mind wandering and attended')
    plt.legend()
    plt.savefig('../data/pupil_size.png')
    plt.show()


def bean_plot():
    x0 = np.load('../data/x0_pupil.npy')
    x1 = np.load('../data/x1_pupil.npy')
    x0 = x0[np.logical_not(np.isnan(x0))]
    x1 = x1[np.logical_not(np.isnan(x1))]
    x = [x0, x1]
    # plt.violinplot(x)
    # plt.xticks(range(4), labels=['', 'mind wandering', 'attended', ''])
    plt.violinplot(x0)
    plt.violinplot(x1)
    plt.ylabel('Pupil Size')
    plt.title('Pupil size of mind wandering and attended')
    plt.legend()
    plt.savefig('../data/pupil_size2.png')
    plt.show()


if __name__ == '__main__':
    # save_data()
    # box_plot()
    bean_plot()
