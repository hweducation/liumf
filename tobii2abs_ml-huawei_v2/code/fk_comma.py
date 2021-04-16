
path_abs = '../data/adjusted_absorbed_states.csv'
path_face = '../data/adjusted_face_states.csv'


def fk_comma(path):
    fin = open(path, 'r')
    tmp = fin.read().replace('，', ',')
    fin.close()
    fout = open(path, 'w')
    fout.write(tmp)


if __name__ == '__main__':
    fk_comma(path_face)
    fk_comma(path_abs)
