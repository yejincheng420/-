from typing import List, Set
from utils import FunctionalDependency
from fc_closure import compute_Fc

def dependency_preserved(original_fds: List[FunctionalDependency], decomposed_fds: List[FunctionalDependency]) -> bool:
    fc_orig = compute_Fc(original_fds)
    fc_dec = compute_Fc(decomposed_fds)
    return fc_orig <= fc_dec