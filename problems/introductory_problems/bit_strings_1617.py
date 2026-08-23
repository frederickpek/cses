import sys
input = sys.stdin.readline
MOD = 1e9 + 7


def solve():
    n = int(input())
    ans = 1
    for _ in range(n):
        ans = int((ans << 1) % MOD)
    print(ans)


if __name__ == "__main__":
    solve()
