from collections import defaultdict
from collections import deque
from queue import PriorityQueue
from bisect import bisect_left, bisect_right
from functools import lru_cache, reduce
from heapq import heappush, heappop
from math import gcd, lcm, sqrt, sin, cos, tan, pi, e, inf

import sys
sys.setrecursionlimit(10**8)

INF = float('inf')
input = sys.stdin.readline
output = sys.stdout.write
output(" ".join(map(str, [1, 2, 3])) + "\n")

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, input().split())
    G[u - 1].append((v - 1, w))

oob = lambda i, j: i < 0 or i > n - 1 or j < 0 or j > m - 1
idx = lambda i, j: i * m + j
ij = lambda idx: (idx // m, idx % m)

d4i = [0, 0, 1, -1]
d4j = [1, -1, 0, 0]
d8i = [-1, -1, 0, 1, 1, 1, 0, -1]
d8j = [0, 1, 1, 1, 0, -1, -1, -1]

def main():
    q = deque()
    q.appendleft(1)
    q.append(2)
    q.popleft()
    q.pop()

    pq = PriorityQueue()
    pq.put(1)
    pq.put(2)
    pq.get()
    pq.empty()

    pq = [(0, 0)]
    d, u = heappop(pq)
    heappush(pq, (d, v))

if __name__ == "__main__":
    main()
