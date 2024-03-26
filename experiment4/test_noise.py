import desbordante
from test_g1 import g1
from test_per_value import per_value
from itertools import permutations
import pandas as pd
import numpy as np


def fd_to_str(fds):
    return set(map(__str__, fds))

SEP = ","
TABLE = '../good_datasets/neighbors10k.csv'


fd = desbordante.Tane()
fd.load_data(TABLE, SEP, False)
fd.execute(error=0)
fds = fd.get_fds()

print(fds)

# to noise all the dataset use following
# df = df.mask(np.random.random(df.shape) < .05)
for fd in fds:
    df = pd.read_csv(TABLE, sep=SEP, header=None)
    for i in fd.lhs_indices:
        col = df.columns[i]
        df.loc[df.sample(frac=0.5).index, col] = np.nan
    df = df.fillna("NULL")

    if len(fd.lhs_indices) == 0: continue
    print(fd, per_value(fd.lhs_indices, fd.rhs_index, df) < g1(fd.lhs_indices, fd.rhs_index, df), per_value(fd.lhs_indices, fd.rhs_index, df))
