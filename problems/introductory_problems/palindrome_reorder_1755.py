import sys
from collections import defaultdict


def solve():
    D = defaultdict(int)
    S = input()
    for c in S: D[c] += 1
    odds = [c for c, f in D.items() if f % 2]
    if len(odds) > 1:
        return print("NO SOLUTION")
    odd = odds[0] if odds else None
    cnt = D[odd]
    del D[odd]
    for c, f in D.items():
        print(c * (f // 2), end="")
    if odd:
        print(odd * cnt, end="")
    for c, f in reversed(D.items()):
        print(c * (f // 2), end="")
    print()

if __name__ == "__main__":
    solve()
