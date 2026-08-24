import sys
from math import inf
input = sys.stdin.readline

"""
This solution TLEs
Passing submissions mostly use 1D distance array instead
"""

def solve():
    n, m, q = map(int, input().split())
    D = [[inf] * n for _ in range(n)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        u, v = u - 1, v - 1
        D[u][v] = min(w, D[u][v])
        D[v][u] = min(w, D[v][u])

    for u in range(n): D[u][u] = 0

    # floyd warshall 
    for k in range(n):
        for u in range(n):
            if D[u][k] == inf: continue
            for v in range(n):
                if D[u][k] + D[k][v] >= D[u][v]: continue
                D[u][v] = D[u][k] + D[k][v]

    for _ in range(q):
        u, v = map(int, input().split())
        ans = D[u - 1][v - 1]
        print(-1 if ans == inf else ans)


if __name__ == "__main__":
    solve()
