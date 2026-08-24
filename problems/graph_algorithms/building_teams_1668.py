import sys
from collections import defaultdict
from collections import deque
input = sys.stdin.readline


def solve():
    n, m = map(int, input().split())
    G = defaultdict(list)
    for _ in range(m):
        u, v = map(int, input().split())
        G[u - 1].append(v - 1)
        G[v - 1].append(u - 1)

    vis = [0] * n

    def dfs(u, col):
        q = deque([u])
        vis[u] = col
        while q:
            u = q.pop()
            for v in G[u]:
                if vis[v]:
                    if vis[u] == vis[v]:
                        return True
                    continue
                q.append(v)
                vis[v] = (vis[u] % 2) + 1

    for u in range(n):
        if not vis[u]:
            if dfs(u, 1):
                print("IMPOSSIBLE")
                return

    print(*vis)


if __name__ == "__main__":
    t = 1 
    # t = int(input())
    for _ in range(t):
        solve()
