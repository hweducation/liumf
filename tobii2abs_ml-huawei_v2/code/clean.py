"""
delete the segments which is not 15s
"""

path_in = '../data/adjusted_absorbed_states.csv'
path_out = '../data/adjusted_absorbed_states.csv'

fin = open(path_in, 'r')
fout = open(path_out, 'w')

for line in fin.readlines():
    elements = line.split(',')
    start, end = float(elements[2]), float(elements[3])
    if start < 0 or end < 0:
        continue
    if end - start != 15:
        continue
    fout.write(line)
