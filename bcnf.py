from typing import List, Set, Tuple
from closure import attribute_closure, is_superkey
from utils import FunctionalDependency, Attribute

# 判定 BCNF

def is_BCNF(rel: Set[Attribute], fds: List[FunctionalDependency]) -> bool:
    """
    判断给定关系模式 rel 在函数依赖 fds 下是否满足 BCNF。
    若所有非平凡依赖的左侧均为超键，则满足 BCNF。
    """
    for lhs, rhs in fds:
        # 如果 lhs 不是超键且存在非主属性依赖，则不满足 BCNF
        if not is_superkey(lhs, rel, fds):
            return False
    return True

# BCNF 分解

def bcnf_decompose(rel: Set[Attribute], fds: List[FunctionalDependency]) -> List[Tuple[Set[Attribute], List[FunctionalDependency]]]:
    """
    对关系模式 rel 及其函数依赖集 fds 进行 BCNF 分解，返回一系列 (子模式, 子模式 FD 列表) 的列表。
    """
    # 若已满足 BCNF，则直接返回
    if is_BCNF(rel, fds):
        return [(rel, fds)]

    # 找到一个违反 BCNF 的依赖 (A -> B)，A 不是超键
    for lhs, rhs in fds:
        if not is_superkey(lhs, rel, fds):
            # 分解 R 为 R1 = A ∪ B, R2 = R - (B - A)
            R1 = lhs | rhs
            R2 = rel - (rhs - lhs)
            # 对应子模式的依赖
            fds1 = [(l, r) for l, r in fds if l.union(r).issubset(R1)]
            fds2 = [(l, r) for l, r in fds if l.union(r).issubset(R2)]
            # 递归分解
            return bcnf_decompose(R1, fds1) + bcnf_decompose(R2, fds2)

    # 若未找到违反的依赖，也说明满足 BCNF
    return [(rel, fds)]