from collections import defaultdict
from collections import deque
from queue import PriorityQueue
from bisect import bisect_left, bisect_right
from functools import lru_cache, reduce
from math import gcd, lcm, sqrt, sin, cos, tan, pi, e, inf

import sys
sys.setrecursionlimit(10**8)

I = lambda: map(int, input().split())

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


if __name__ == "__main__":
    main()
