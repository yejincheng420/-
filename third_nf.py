from typing import List, Set, Tuple
from closure import attribute_closure, candidate_keys
from utils import FunctionalDependency, Attribute

# 最小覆盖

def minimal_cover(fds: List[FunctionalDependency]) -> List[FunctionalDependency]:
    """
    计算函数依赖集的最小覆盖：
    1. 将 RHS 拆分为单属性依赖；
    2. 消除 LHS 中的冗余属性（仅在 |LHS| > 1 时）；
    3. 删除多余的依赖。"""
    # 1. 单属性 RHS
    fds1: List[FunctionalDependency] = []
    for lhs, rhs in fds:
        for attr in rhs:
            fds1.append((set(lhs), {attr}))

    # 2. 消除 LHS 冗余属性
    fds2: List[FunctionalDependency] = []
    for lhs, rhs in fds1:
        new_lhs = set(lhs)
        # 仅当 LHS 大小 >1 时才尝试去掉属性
        if len(lhs) > 1:
            for attr in list(lhs):
                test_lhs = new_lhs - {attr}
                # 使用当前剩余的依赖来测试
                other_fds = fds1.copy()
                other_fds.remove((lhs, rhs))
                if rhs.issubset(attribute_closure(test_lhs, other_fds + [(test_lhs, rhs)])):
                    new_lhs.remove(attr)
        fds2.append((new_lhs, rhs))

    # 3. 删除多余的依赖
    fds3 = fds2.copy()
    for fd in fds2:
        lhs, rhs = fd
        test_fds = fds3.copy()
        test_fds.remove(fd)
        if rhs.issubset(attribute_closure(lhs, test_fds)):
            fds3.remove(fd)

    return fds3

# 3NF 分解

def third_nf_decompose(all_attrs: Set[Attribute], fds: List[FunctionalDependency]) -> List[Tuple[Set[Attribute], List[FunctionalDependency]]]:
    """
    对模式进行 3NF 分解：
    1. 计算最小覆盖；
    2. 根据每个 FD 构造子模式；
    3. 若没有子模式包含候选码，则添加一个包含候选码的子模式。
    """
    mc = minimal_cover(fds)
    schemas: List[Tuple[Set[Attribute], List[FunctionalDependency]]] = []
    for lhs, rhs in mc:
        schemas.append((lhs | rhs, [(lhs, rhs)]))

    # 若无子模式包含候选码，则添加
    keys = candidate_keys(all_attrs, fds)
    # 只需确保至少有一个子模式包含某个候选码
    if not any(key.issubset(schema_attrs) for key in keys for schema_attrs, _ in schemas):
        schemas.append((keys[0], []))

    return schemas