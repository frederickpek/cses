import sys
from collections import deque
input = sys.stdin.readline

d4i = [1, -1, 0, 0]
d4j = [0, 0, 1, -1]


def solve():
    n, m = map(int, input().split())
    idx = lambda i, j: i * m + j
    oob = lambda i, j: i < 0 or i > n - 1 or j < 0 or j > m - 1
    G = list()
    si, sj = -1, -1
    mij = list()
    vis_m = [0] * (n * m)
    for i in range(n):
        row = list(input())
        for j in range(m):
            if row[j] == "A":
                si, sj = i, j
            elif row[j] == "M":
                vis_m[idx(i, j)] = 1
                mij.append((i, j))
        G.append(row)

    mq = deque(mij)
    pq = deque([(si, sj)])
    vis_p = [0] * (n * m)
    P = [-1] * (n * m)
    vis_p[idx(si, sj)] = 1

    def step_monster():
        next_q = deque()
        while mq:
            i, j = mq.pop()
            for k in range(4):
                di = i + d4i[k]
                dj = j + d4j[k]
                if oob(di, dj) or G[di][dj] == "#" or vis_m[idx(di, dj)]: continue
                next_q.append((di, dj))
                vis_m[idx(di, dj)] = 1
        mq.extend(next_q)

    def step_player():
        next_q = deque()
        while pq:
            i, j = pq.pop()
            if i == 0 or i == n - 1 or j == 0 or j == m - 1:
                return (i, j)
            for k in range(4):
                di = i + d4i[k]
                dj = j + d4j[k]
                if oob(di, dj) or G[di][dj] == "#": continue
                if vis_p[idx(di, dj)] or vis_m[idx(di, dj)]: continue
                next_q.append((di, dj))
                vis_m[idx(di, dj)] = 1
                P[idx(di, dj)] = idx(i, j)
        pq.extend(next_q)

    def print_sol(i, j):
        print("YES")
        ans = list()
        curr = idx(i, j)
        while P[curr] != -1:
            prev = P[curr]
            if prev + 1 == curr:
                ans.append("R")
            elif prev - 1 == curr:
                ans.append("L")
            elif prev > curr:
                ans.append("U")
            else:
                ans.append("D")
            curr = prev
        print(len(ans))
        print("".join(ans[::-1]))

    while pq:
        step_monster()
        ij = step_player()
        if ij:
            print_sol(*ij)
            return

    print("NO")


if __name__ == "__main__":
    t = 1 
    # t = int(input())
    for _ in range(t):
        solve()
