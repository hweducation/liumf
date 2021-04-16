import matplotlib.pyplot as plt


def plot_():
    path = '../data/ranking.csv'
    x = []
    y = [[] for ii in range(4)]
    f = open(path, 'r')
    for line in f.readlines():
        elements = line.split(',')
        x.append(int(elements[0]))
        for jj in range(4):
            y[jj].append(float(elements[jj + 1]))

    names = ['acc', 'recall', 'f1', 'ROC']
    for i in range(4):
        plt.plot(x, y[i])
        plt.title(names[i])
        plt.xlabel('number of features(ranked)')
        plt.ylabel(names[i])
        plt.savefig('../data/pics/' + names[i])
        plt.close()


plot_()


"""
分成10组
51个人
每次有九个组训练,一个组测试
"""