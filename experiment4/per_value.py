# lhs = [0,2,3]
# rhs = 1
# filename = '../build/target/input_data/iris.csv'

import pandas as pd

def per_value(lhs, rhs, filename, SEP):
    df = pd.read_csv(filename, sep=SEP, header=None)
    data = df.groupby(lhs).groups

    S = 0
    for a in data:
        rows = data[a].to_list()
        y_values = df.loc[rows].groupby([rhs]).groups
        y_counts = set(map(lambda k: len(y_values[k]), y_values))
        S += max(y_counts)/len(rows)

    S = 1 - S/len(data)
    return S
    # print("error PerValue(", lhs, "->", rhs, ") =", )