import desbordante
from g1 import g1
from per_value import per_value
from itertools import permutations
import pandas as pd

def fd_to_str(fds):
    return set(map(__str__, fds))

SEP = ","
TABLE = '../good_datasets/neighbors10k.csv'
NUM_ATTRS = 7
MAX_LHS = 1

df = pd.read_csv(TABLE, sep=SEP, header=None)
for p in permutations(range(NUM_ATTRS), MAX_LHS+1):
    rhs = p[-1]
    lhs = list(p[:-1])
    
    print(lhs, "->", rhs, g1(lhs, rhs, df) > per_value(lhs, rhs, df))


