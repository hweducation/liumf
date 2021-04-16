import pandas as pd

data = pd.read_csv('../data/hz.csv', encoding='gbk')
print(data.shape)
dict1 = {}
for i in range(data.shape[0]):
    tmp = data.values[i][6]
    elements = tmp.split(',')
    for ele in elements:
        dict1[ele] = 1
print(len(dict1))
print(dict1)
