import desbordante
from g1 import g1
from per_value import per_value


def fd_to_str(fds):
    return set(map(__str__, fds))

SEP = ","
TABLE = 'test.csv'
# TABLE = 'test.csv'
ERROR = 0.1

pfd = desbordante.PFDTane()
pfd.load_data(TABLE, SEP, True)
pfd.set_option("error_measure", "per_value")
pfd.execute(error=ERROR)
pfds = pfd.get_fds()



afd = desbordante.Tane()
afd.load_data(TABLE, SEP, True)
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

    # pv_ = per_value(fd.lhs_indices, fd.rhs_index, TABLE, SEP)
    # g1_ = g1(fd.lhs_indices, fd.rhs_index, TABLE, SEP)
    # print(fd, " g1(fd)=", g1_)
        

# возвратит pfds - afds
# то есть те pFD, которые не являются AFD (с данным порогом ошибки) 
print(diff(pfds, afds))
        
