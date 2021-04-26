import pandas as pd
import time


def combine():
    def bit_op(lst1, lst2):
        tmp = [0] * len(lst1)
        for i in range(len(lst1)):
            tmp[i] = lst1[i] | lst2[i]
        return tmp

    path_abs = '../data/adjusted_absorbed_states.csv'
    path_face = '../data/adjusted_face_states.csv'
    out_path = '../data/abs_with_face.csv'
    absorb = pd.read_csv(path_abs, encoding='gbk')
    face = pd.read_csv(path_face, encoding='gbk')
    absorb.sort_values(by=['name', 'start_time'], inplace=True)
    face.sort_values(by=['name', 'start_time'], inplace=True)
    print('sorting finished')
    fout = open(out_path, 'w')
    len_abs = absorb.shape[0]
    len_face = face.shape[0]
    i_abs, i_face = 0, 0
    while i_abs < len_abs:
        now_name = face.values[i_face][0]
        print(now_name)
        bit_map = [[0] * 17 for _ in range(10000)]
        try:
            while face.values[i_face][0] == now_name:
                face_states = [0] * 17
                for x in face.values[i_face][1].split(','):
                    face_states[int(x) - 1] = 1
                for x in range(int(float(face.values[i_face][2])), int(float(face.values[i_face][3])) + 1):
                    bit_map[x] = face_states
                i_face += 1
        except IndexError:
            pass

        try:
            while absorb.values[i_abs][0] == now_name:
                face_states = [0] * 17
                for x in range(int(float(absorb.values[i_abs][2])), int(float(absorb.values[i_abs][3])) * 1):
                    face_states = bit_op(face_states, bit_map[x])
                face_states = [str(x) for x in face_states]
                fout.write('{},{},{},{},{},\n'.format(absorb.values[i_abs][0],
                                                      absorb.values[i_abs][1],
                                                      absorb.values[i_abs][2],
                                                      absorb.values[i_abs][3],
                                                      ','.join(face_states)))
                i_abs += 1
        except IndexError:
            pass


if __name__ == '__main__':
    combine()
