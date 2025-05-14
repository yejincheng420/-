from typing import Set, List
from utils import FunctionalDependency, Attribute

def attribute_closure(attrs: Set[Attribute], fds: List[FunctionalDependency]) -> Set[Attribute]:
    closure = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(closure) and not rhs.issubset(closure):
                closure |= rhs
                changed = True
    return closure

# 超码与候选码判定

def is_superkey(attrs: Set[Attribute], all_attrs: Set[Attribute], fds: List[FunctionalDependency]) -> bool:
    return attribute_closure(attrs, fds) == all_attrs

# 获取所有候选码

def candidate_keys(all_attrs: Set[Attribute], fds: List[FunctionalDependency]) -> List[Set[Attribute]]:
    from itertools import combinations
    keys = []
    for r in range(1, len(all_attrs)+1):
        for combo in combinations(all_attrs, r):
            combo = set(combo)
            if is_superkey(combo, all_attrs, fds):
                # 最小性
                if not any(prev.issubset(combo) for prev in keys):
                    keys.append(combo)
    return keys