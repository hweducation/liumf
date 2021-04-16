import pandas as pd


def combine():
    path_abs = '../data/adjusted_absorbed_states.csv'
    path_face = '../data/adjusted_face_states.csv'
    out_path = '../data/abs_with_face.csv'
    absorb = pd.read_csv(path_abs, encoding='gbk')
    face = pd.read_csv(path_face, encoding='gbk')
    fout = open(out_path, 'w')
    len_abs = absorb.shape[0]
    len_face = face.shape[0]
    i_abs, i_face = 0, 0
    face_states = ['0'] * 17
    while i_abs < len_abs:
        if i_face >= len_face:
            fout.write('{},{},{},{},{},\n'.format(absorb.values[i_abs][0],
                                                  absorb.values[i_abs][1],
                                                  absorb.values[i_abs][2],
                                                  absorb.values[i_abs][3],
                                                  ','.join(face_states)))
            i_abs += 1
            continue
        if absorb.values[i_abs][0] != face.values[i_face][0]:
            if absorb.values[i_abs][0] > face.values[i_face][0]:
                i_face += 1
            else:
                fout.write('{},{},{},{},{},\n'.format(absorb.values[i_abs][0],
                                                      absorb.values[i_abs][1],
                                                      absorb.values[i_abs][2],
                                                      absorb.values[i_abs][3],
                                                      ','.join(face_states)))
                i_abs += 1
                face_states = ['0'] * 17
            continue
        if absorb.values[i_abs][3] < face.values[i_face][2]:
            fout.write('{},{},{},{},{},\n'.format(absorb.values[i_abs][0],
                                                  absorb.values[i_abs][1],
                                                  absorb.values[i_abs][2],
                                                  absorb.values[i_abs][3],
                                                  ','.join(face_states)))
            i_abs += 1
            face_states = ['0'] * 17
            continue
        if absorb.values[i_abs][2] > face.values[i_face][3]:
            i_face += 1
            continue
        for tmp in face.values[i_face][1].split(','):
            face_states[int(tmp) - 1] = '1'
        i_face += 1


if __name__ == '__main__':
    combine()
