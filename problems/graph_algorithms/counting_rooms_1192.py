from collections import deque

d4i = [1, -1, 0, 0]
d4j = [0, 0, 1, -1]


def solve():
    n, m = map(int, input().split())
    oob = lambda i, j: i < 0 or i > n - 1 or j < 0 or j > m - 1
    G = list()
    for _ in range(n): G.append(list(input()))

    q = deque()
    vis = [0] * (n * m)
    idx = lambda i, j: i * m + j

    def dfs(i, j):
        vis[idx(i, j)] = 1
        q = deque([(i, j)])

        while q:
            i, j = q.pop()
            for k in range(4):
                di = i + d4i[k]
                dj = j + d4j[k]
                if oob(di, dj) or G[di][dj] != "." or vis[idx(di, dj)]: continue
                q.append((di, dj))
                vis[idx(di, dj)] = 1

    ans = 0
    for i in range(n):
        for j in range(m):
            if G[i][j] == "." and not vis[idx(i, j)]:
                dfs(i, j)
                ans += 1

    print(ans)


if __name__ == "__main__":
    solve()
