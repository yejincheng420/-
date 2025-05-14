from typing import List, Tuple, Set
from closure import attribute_closure
from utils import FunctionalDependency

def fd_in_closure(fd: FunctionalDependency, fds: List[FunctionalDependency]) -> bool:
    lhs, rhs = fd
    return rhs.issubset(attribute_closure(lhs, fds))

# 计算 FD 集闭包

def compute_Fc(fds: List[FunctionalDependency]) -> Set[FunctionalDependency]:
    closure = set()
    for lhs, rhs in fds:
        for attr in rhs:
            if fd_in_closure((lhs, {attr}), fds):
                closure.add((lhs, {attr}))
    return closure