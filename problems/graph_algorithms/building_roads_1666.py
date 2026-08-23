import sys
from collections import deque
from collections import defaultdict
input = sys.stdin.readline


def solve():
    G = defaultdict(list)
    n, m = map(int, input().split())
    for _ in range(m):
        u, v = map(int, input().split())
        G[u - 1].append(v - 1)
        G[v - 1].append(u - 1)

    C = [-1] * n

    def dfs(u, c):
        C[u] = c
        q = deque([u])
        while q:
            u = q.pop()
            for v in G[u]:
                if C[v] != -1: continue
                q.append(v)
                C[v] = c

    c = 0
    T = list()
    for u in range(n):
        if C[u] != -1: continue
        dfs(u, c)
        c += 1
        T.append(u)

    print(c - 1)
    for i in range(c - 1):
        print(T[i] + 1, T[i + 1] + 1)


if __name__ == "__main__":
    solve()
