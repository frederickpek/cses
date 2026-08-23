import sys
input = sys.stdin.readline

"""
    "Z0000" = Z * (2 * 5)^4
    need to find pairs of 2,5s in the resulting factorial
    since 2 always precedes 5 under factorials
    we just need count numbers from 1 to n with 5 in their prime factorisation and occurrence accordingly
"""

def solve():
    n = int(input())
    ans = 0
    while n:
        n //= 5
        ans += n
    print(ans)


if __name__ == "__main__":
    solve()
