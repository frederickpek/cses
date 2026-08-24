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
    P = [-1] * n

    def dfs(u):
        q = deque([u])
        while q:
            u = q.pop()
            if vis[u]: continue
            vis[u] = 1
            for v in G[u]:
                if vis[v]:
                    if P[u] != v:
                        ans = [v + 1]
                        curr = u
                        while True:
                            ans.append(curr + 1)
                            if curr == v:
                                print(len(ans))
                                print(*ans)
                                return True
                            curr = P[curr]
                    continue
                q.append(v)
                P[v] = u


    for u in range(n):
        if not vis[u]:
            if dfs(u):
                return


    print("IMPOSSIBLE")

if __name__ == "__main__":
    t = 1 
    # t = int(input())
    for _ in range(t):
        solve()
