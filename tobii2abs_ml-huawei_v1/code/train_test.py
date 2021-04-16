import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier


def del_invalid(samples):
    new_samples = []
    for tmp in samples:
        if 0 not in tmp[:-1]:
            new_samples.append(tmp)
    return np.array(new_samples)


def main():
    np.random.seed(3)

    abs0 = np.load('../data/sample_0.npy')
    abs1 = np.load('../data/sample_1.npy')
    abs0 = np.c_[abs0, np.zeros(abs0.shape[0], dtype=int).T]
    abs1 = np.c_[abs1, np.ones(abs1.shape[0], dtype=int).T]
    print(abs0.shape)
    print(abs1.shape)

    abs0 = del_invalid(abs0)
    abs1 = del_invalid(abs1)
    row_rand_array = np.arange(abs1.shape[0])
    np.random.shuffle(row_rand_array)
    abs1 = abs1[row_rand_array[:abs0.shape[0]]]
    print(abs0.shape)
    print(abs1.shape)

    samples = np.concatenate((abs0, abs1), axis=0)
    samples[np.isnan(samples)] = 0

    row_rand_array = np.arange(samples.shape[0])
    np.random.shuffle(row_rand_array)
    samples = samples[row_rand_array]

    # samples1 = samples

    offset0 = int(samples.shape[0] * 0.8)
    offset1 = int(samples.shape[0] * 0.9)

    # clf = LogisticRegression()
    # clf = GaussianNB()
    # clf = SVC()
    # clf = MLPClassifier()
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    # clf = RandomForestClassifier()

    clf.fit(samples[0:offset0, :-1], samples[0:offset0, -1])
    # tree.plot_tree(clf)

    prd = clf.predict(samples[offset0:offset1, :-1])
    print(accuracy_score(samples[offset0:offset1:, -1], prd))
    print(recall_score(samples[offset0:offset1, -1], prd))
    print(f1_score(samples[offset0:offset1, -1], prd))
    print(roc_auc_score(samples[offset0:offset1, -1], prd))

    print()
    prd = clf.predict(samples[offset1:, :-1])
    print(accuracy_score(samples[offset1:, -1], prd))
    print(recall_score(samples[offset1:, -1], prd))
    print(f1_score(samples[offset1:, -1], prd))
    print(roc_auc_score(samples[offset1:, -1], prd))


if __name__ == '__main__':
    main()
