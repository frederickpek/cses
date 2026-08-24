import sys
input = sys.stdin.readline


def solve():
    n = int(input())
    A = [0] * n
    indeg = [0] * n
    P = list(map(lambda x: int(x) - 1, input().split()))
    for u, p in enumerate(P):
        indeg[p] += 1

    q = list()
    for u, d in enumerate(indeg):
        if d: continue
        q.append(u)

    while q:
        u = q.pop()
        if not u: break
        p = P[u - 1]
        A[p] += A[u] + 1
        indeg[p] -= 1
        if not indeg[p]:
            q.append(p)

    print(*A)


if __name__ == "__main__":
    solve()
