# lhs = [0,2,3]
# rhs = 1
# filename = '../build/target/input_data/iris.csv'

import pandas as pd

def num_pairs(n):
    return (n-1)*n/2 

def g1(lhs, rhs, filename, SEP):
    df = pd.read_csv(filename, sep=SEP, header=None)
    data = df.groupby(lhs).groups

    S = 0
    for a in data:
        rows = data[a].to_list()
        if len(rows) == 1: continue
        y_values = df.loc[rows].groupby([rhs]).groups
        y_counts = map(lambda k: len(y_values[k]), y_values)
        S += num_pairs(len(rows))
        for c in y_counts:
            S -= num_pairs(c)
    S =  S/num_pairs(len(df))
    return S
    # print("error e(", lhs, "->", rhs, ") =", S)