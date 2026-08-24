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
