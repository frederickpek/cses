import sys
input = sys.stdin.readline


def solve():
    i, j = map(int, input().split())
    p = min(i, j)
    q = max(i, j)
    # even: clockwise
    # odd: anticlockwise
    """
        ring candidates:
            lo = (q - 1) ** 2 + 1
            hi = q ** 2
        
        mirror candidates:
            lo + p - 1
            hi - p + 1
        
        if i > j:
            if q even:
                ans = hi - p + 1
            else:
                ans = lo + p - 1
        else:
            if q even:
                ans = lo + p - 1
            else:
                ans = hi - p + 1
    """
    if (i > j and q % 2 == 0) or (i < j and q % 2 != 0):
        print(q ** 2 - p + 1)
    else:
        print((q - 1) ** 2 + p)


if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
