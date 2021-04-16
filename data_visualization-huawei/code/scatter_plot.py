"""
step 5
scatter plot
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def get_fixation_point(path):
    x, y, tmp_x, tmp_y = [], [], [], []
    f = open(path, 'r')
    for line in f.readlines():
        if line == '\n':
            if np.mean(tmp_x) != 0:
                x.append(np.mean(tmp_x))
                y.append(np.mean(tmp_y))
            tmp_x.clear()
            tmp_y.clear()
            continue
        elements = line.split(',')[:-1]
        if elements[26] != '' and elements[27] != '':
            try:
                tmp_x.append(int(elements[26]))
                tmp_y.append(int(elements[27]))
            except ValueError:
                continue
    f.close()
    return np.array(x), np.array(y)


# gaze point 26,27 pupil diameter left,right 38,39(start form 0)
def save_data():
    path0 = '../data/abs_0.csv'
    path1 = '../data/abs_1.csv'
    x0, y0 = get_fixation_point(path0)
    np.save('../data/x0.npy', x0)
    np.save('../data/y0.npy', y0)
    x1, y1 = get_fixation_point(path1)
    np.save('../data/x1.npy', x1)
    np.save('../data/y1.npy', y1)


def del_nan(x):
    return x[np.logical_not(np.isnan(x))]


def scatter_plot():
    x0, y0 = np.load('../data/x0.npy'), np.load('../data/y0.npy')
    x1, y1 = np.load('../data/x1.npy'), np.load('../data/y1.npy')
    x0, y0 = del_nan(x0), del_nan(y0)
    x1, y1 = del_nan(x1), del_nan(y1)
    data0 = pd.DataFrame({'x': x0, 'y': y0})
    data1 = pd.DataFrame({'x': x1, 'y': y1})

    plt.plot('x', 'y', "", data=data0, linestyle='', marker='.', color='g', markersize=2, label='mind wandering')
    plt.plot('x', 'y', "", data=data1.sample(4634, random_state=1), linestyle='', marker='.', color='r', markersize=2,
             label='attended')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Gaze point of mind wandering and attended')
    plt.legend()
    plt.show()
    # plt.savefig('../data/scatter.png')


if __name__ == '__main__':
    # save_data()
    scatter_plot()
