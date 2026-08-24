import sys
from math import inf
from collections import defaultdict
from queue import PriorityQueue
input = sys.stdin.readline


def solve():
    n, m = map(int, input().split())
    G = defaultdict(list)
    for _ in range(m):
        u, v, w = map(int, input().split())
        G[u - 1].append((v - 1, w))

    D = [inf] * n
    pq = PriorityQueue()
    pq.put((0, 0))
    D[0] = 0

    while not pq.empty():
        d, u = pq.get()
        if D[u] != d: continue
        for v, w in G[u]:
            if D[u] + w >= D[v]: continue
            D[v] = D[u] + w
            pq.put((D[v], v))

    print(*D)


if __name__ == "__main__":
    t = 1 
    # t = int(input())
    for _ in range(t):
        solve()
