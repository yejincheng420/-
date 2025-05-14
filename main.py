import argparse
from closure import attribute_closure, candidate_keys, is_superkey
from fc_closure import fd_in_closure, compute_Fc
from fd_preserve import dependency_preserved
from bcnf import is_BCNF, bcnf_decompose
from third_nf import third_nf_decompose
from utils import FunctionalDependency

def parse_fd(fd_str: str) -> FunctionalDependency:
    lhs, rhs = fd_str.split('->')
    return set(lhs.strip()), set(rhs.strip())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='范式理论工具')
    parser.add_argument('--attributes', required=True, help='属性集，如 ABC')
    parser.add_argument('--fds', nargs='+', required=True, help="函数依赖，如 A->B B->C")
    args = parser.parse_args()
    attrs = set(args.attributes)
    fds = [parse_fd(s) for s in args.fds]

    print('属性闭包举例：', attribute_closure({'A'}, fds))
    print('候选码：', candidate_keys(attrs, fds))
    print('BCNF 判定：', is_BCNF(attrs, fds))
    print('BCNF 分解：', bcnf_decompose(attrs, fds))
    print('3NF 分解：', third_nf_decompose(attrs, fds))