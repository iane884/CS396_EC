## compute.py
# contains helper functions to check winning coalitions and compute shapley/banzhaf indices

import math
from itertools import combinations, permutations


def is_winning(coalition, k, quotas, W):
    for dim in range(k):
        total = sum(W[dim][i] for i in coalition)
        if total < quotas[dim]:
            return False
    return True


def compute_banzhaf(k, quotas, W):
    n = len(W[0])
    raw = [0] * n
    players = list(range(n))
    # enumerate all coalitions
    for r in range(n + 1):
        for combo in combinations(players, r):
            S = set(combo)
            # skip if s is already winning
            if is_winning(S, k, quotas, W):
                continue
            # else: for each i not in S, check if adding i makes it winning
            for i in players:
                if i in S:
                    continue
                if is_winning(S.union({i}), k, quotas, W):
                    raw[i] += 1
    total = sum(raw)
    if total > 0:
        return [r / total for r in raw]
    else:
        # no winning coalition
        return [0.0] * n


def compute_shapley(k, quotas, W):
    n = len(W[0])
    shap = [0] * n
    players = list(range(n))
    factorial_n = math.factorial(n)
    # enumerate all permutations
    for perm in permutations(players):
        coalition = set()
        for i in perm:
            if not is_winning(coalition, k, quotas, W) and \
               is_winning(coalition.union({i}), k, quotas, W):
                shap[i] += 1
            coalition.add(i)
    # normalize by n!
    if factorial_n > 0:
        return [s / factorial_n for s in shap]
    else:
        return [0.0] * n