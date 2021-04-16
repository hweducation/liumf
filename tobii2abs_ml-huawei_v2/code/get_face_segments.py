from tool import *
import pandas as pd


def get_face_segments(path, out_path):
    ori_names = get_file_names(path)
    names = [x[22:-15] for x in ori_names]
    fout = open(out_path, 'w')
    for i_name in range(len(ori_names)):
        absorbed_data = pd.ExcelFile(path + ori_names[i_name]).parse(sheet_name=1)
        for i in range(absorbed_data.size - 1):
            try:
                start1 = get_sec(absorbed_data.values[i][7])
                end1 = get_sec(absorbed_data.values[i][8])
            except IndexError:
                continue
            score = absorbed_data.values[i][6]
            name = names[i_name]
            if score == 0 or score == '0':
                continue
            fout.write(name + ',"' + str(score) + '",' + str(start1) + ',' + str(end1) + ',\n')
    fout.close()


if __name__ == '__main__':
    path1 = 'E:\\data\\数据堂-总\\'
    out_path1 = '../data/face_segments.csv'
    get_face_segments(path1, out_path1)
