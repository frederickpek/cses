import sys
from collections import deque
input = sys.stdin.readline

d4i = [1, -1, 0, 0]
d4j = [0, 0, 1, -1]


def solve():
    n, m = map(int, input().split())
    oob = lambda i, j: i < 0 or i > n - 1 or j < 0 or j > m - 1
    G = list()
    si, sj, ti, tj = -1, -1, -1, -1
    for i in range(n):
        row = list(input())
        G.append(row)
        for j in range(m):
            if row[j] == "A":
                si, sj = i, j
            if row[j] == "B":
                ti, tj = i, j


    q = deque([(si, sj)])
    vis = [0] * (n * m)
    P = [-1] * (n * m)
    idx = lambda i, j: i * m + j
    vis[idx(si, sj)] = 1

    def yes():
        print("YES")
        curr = idx(ti, tj)
        steps = list()
        while P[curr] != -1:
            prev = P[curr]
            if prev + 1 == curr:
                steps.append("R")
            elif prev - 1 == curr:
                steps.append("L")
            elif prev > curr:
                steps.append("U")
            else:
                steps.append("D")
            curr = prev
        print(len(steps))
        print("".join(steps[::-1]))

    while q:
        i, j = q.popleft()
        if i == ti and j == tj:
            return yes()
        for k in range(4):
            di = i + d4i[k]
            dj = j + d4j[k]
            if oob(di, dj) or G[di][dj] == "#" or vis[idx(di, dj)]: continue
            P[idx(di, dj)] = idx(i, j)
            q.append((di, dj))
            vis[idx(di, dj)] = 1

    print("NO")


if __name__ == "__main__":
    solve()
