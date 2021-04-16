"""
step 2
Get segments and labels from k4a recording device
Save it in 'absorbed_segments.csv'
That program needs a few seconds to run.
"""
import os
import pandas as pd
from tool import *


def get_segments(path, out_path):
    ori_names = get_file_names(path)
    names = [x[22:-15] for x in ori_names]
    fout = open(out_path, 'w')
    fout.write('name,absorbed_score,start_time,end_time\n')
    for i_name in range(len(ori_names)):
        absorbed_data = pd.ExcelFile(path + ori_names[i_name]).parse(sheet_name=2)
        for i in range(absorbed_data.size - 1):
            try:
                start1 = get_sec(absorbed_data.values[i][7])
                end1 = get_sec(absorbed_data.values[i][8])
            except IndexError:
                continue
            score = absorbed_data.values[i][6]
            name = names[i_name]
            fout.write(name + ',' + str(score) + ',' + str(start1) + ',' + str(end1) + ',\n')
    fout.close()


if __name__ == '__main__':
    path1 = 'E:\\data\\数据堂-总\\'
    out_path1 = '../data/absorbed_segments.csv'
    get_segments(path1, out_path1)
