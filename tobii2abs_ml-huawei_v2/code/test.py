import numpy as np
import pandas as pd


def amazing_work():
    lst0 = []
    for i in range(17):
        lst0.append('Facial Feature={}'.format(i + 1))
    lst1 = []
    methods = ['Mean', 'Maximum', 'Minimum', 'Median', 'Standard Deviation',
               'Skewness', 'Kurtosis']
    lst1 += ['Gaze Point Left', 'Gaze Point Right']
    gaze_d = ['Gaze Direction Left', 'Gaze Direction Right']
    gaze_direction = ['x', 'y', 'z']
    for aa in gaze_d:
        for bb in gaze_direction:
            lst1.append(aa + ' ' + bb)
    lst1 += ['Pupil Diameter Left', 'Pupil Diameter Right']

    ans = lst0

    for aa in lst1:
        for bb in methods:
            ans.append(aa + ' ' + bb)

    ans += [x + ' Duration' for x in ['Fixation', 'Saccade', 'Unclassified', 'EyesNotFound']]
    # print(ans)

    nums = """
    13  0 12  4 16 11  3  2  1 76 77 82 86 74 75 73 79 10 78 85  5 81 84 83
      7 50  9 15 71 41 62 34 43 80 36 59 52 55 57 31 69 67 38 48 39 44 61 64
     45 51 40 46 65 32  6 60 53 87 66 33 72 37 54 58 49 68 47 42 56 63 35  8
     70 14 30 20 22 18 23 17 26 21 25 28 24 29 19 27 88 89 90
     """
    nums = [int(x) for x in nums.split()]

    nums = np.array(nums)
    nums = 90 - nums

    final = [''] * 91

    for i in range(91):
        final[nums[i]] = ans[i]
    print(final)
    fout = open('../data/features.txt', 'w')
    fout.write('\n'.join(final))
    fout.close()


a = np.load('../data/v2_array.npy')
print(a.shape)

