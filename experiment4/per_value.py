# lhs = [0,2,3]
# rhs = 1
# filename = '../build/target/input_data/iris.csv'

import pandas as pd

def per_value(lhs, rhs, df):
    
    data = df.groupby(lhs).groups

    S = 0
    for a in data:
        if len(data[a]) == 1: 
            S+=1
            continue
        rows = data[a].to_list()
        y_values = df.loc[rows].groupby([rhs]).groups
        y_counts = set(map(lambda k: len(y_values[k]), y_values))
        try:
            S += max(y_counts)/len(rows)
        except:
            print("problem with nulls")
            quit()

    S = 1 - S/len(data)
    return S
    # print("error PerValue(", lhs, "->", rhs, ") =", )