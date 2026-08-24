import sys
from collections import defaultdict
from collections import deque
input = sys.stdin.readline


def solve():
    n, m = map(int, input().split())
    G = defaultdict(list)
    for _ in range(m):
        u, v = map(int, input().split())
        G[u].append(v)
        G[v].append(u)

    # bfs + backtracking
    
    P = [-1] * (n + 1)
    vis = [0] * (n + 1)
    q = deque([1])
    vis[1] = 1

    def print_ans():
        curr = n
        ans = [curr]
        while P[curr] != -1:
            prev = P[curr]
            ans.append(prev)
            curr = prev
        print(len(ans))
        print(" ".join(map(str, ans[::-1])))

    while q:
        u = q.popleft()
        if u == n:
            return print_ans()
        for v in G[u]:
            if vis[v]: continue
            q.append(v)
            vis[v] = 1
            P[v] = u

    print("IMPOSSIBLE")


if __name__ == "__main__":
    t = 1 
    # t = int(input())
    for _ in range(t):
        solve()
