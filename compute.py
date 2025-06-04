## 2. `compute.py`
# Contains helper functions to check winning coalitions and compute Shapley or Banzhaf indices.


# compute.py
import math
from itertools import combinations, permutations


def is_winning(coalition, k, quotas, W):
    """
    coalition: a set of player indices (0..n-1)
    k: number of dimensions
    quotas: list of k integers
    W: k x n weight matrix (W[dim][player])
    Returns True if coalition meets all dimension quotas.
    """
    for dim in range(k):
        total = sum(W[dim][i] for i in coalition)
        if total < quotas[dim]:
            return False
    return True


def compute_banzhaf(k, quotas, W):
    """
    Returns a normalized Banzhaf index list of length n (floats summing to 1).
    """
    n = len(W[0])
    raw = [0] * n
    players = list(range(n))
    # Enumerate all coalitions S of any size r
    for r in range(n + 1):
        for combo in combinations(players, r):
            S = set(combo)
            # If S already winning, skip (no one is critical)
            if is_winning(S, k, quotas, W):
                continue
            # Otherwise, for each i not in S, check if adding i makes it winning
            for i in players:
                if i in S:
                    continue
                if is_winning(S.union({i}), k, quotas, W):
                    raw[i] += 1
    total = sum(raw)
    if total > 0:
        return [r / total for r in raw]
    else:
        # No winning coalition at all (degenerate); return zeros
        return [0.0] * n


def compute_shapley(k, quotas, W):
    """
    Returns Shapley values (floats summing to 1) for each player index 0..n-1.
    """
    n = len(W[0])
    shap = [0] * n
    players = list(range(n))
    factorial_n = math.factorial(n)
    # Enumerate all permutations (n! of them)
    for perm in permutations(players):
        coalition = set()
        for i in perm:
            if not is_winning(coalition, k, quotas, W) and \
               is_winning(coalition.union({i}), k, quotas, W):
                shap[i] += 1
            coalition.add(i)
    # Normalize by n!
    if factorial_n > 0:
        return [s / factorial_n for s in shap]
    else:
        return [0.0] * n