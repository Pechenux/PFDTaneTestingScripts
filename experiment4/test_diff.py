import desbordante
from g1 import g1
from per_value import per_value
from itertools import permutations
import pandas as pd

def fd_to_str(fds):
    return set(map(__str__, fds))

SEP = ","
TABLE = '../good_datasets/neighbors10k.csv'
df = pd.read_csv(TABLE, sep=SEP, header=None)


for ERROR in [0.01, 0.05, 0.1, 0.2, 0.3]:
    for measure in ["per_value"]:
            pfd = desbordante.PFDTane()
            pfd.load_data(TABLE, SEP, False)
            pfd.set_option("error_measure", measure)
            pfd.execute(error=ERROR)
            pfds = pfd.get_fds()



            afd = desbordante.Tane()
            afd.load_data(TABLE, SEP, False)
            afd.execute(error=ERROR)
            afds = afd.get_fds()


            def diff(pfds, afds):
                res = set()
                for pfd_ in (pfds):
                    found = False # нашли ли эту pFD среди минимальных AFD и производных
                    for afd_ in (afds):
                        if afd_.rhs_index == pfd_.rhs_index and  set(afd_.lhs_indices) <= set(pfd_.lhs_indices):
                            found = True
                            break
                        
                    if not found:
                        res.add(pfd_)
                return res

            print(diff(pfds, afds))
