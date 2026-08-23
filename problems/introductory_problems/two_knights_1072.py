import sys, math
input = sys.stdin.readline


def solve():
    n = int(input())
    for k in range(1, n + 1):
        # knights are not unique
        # total kC2 ways of placing knights
        # remove 2x3 vertical and horizontal tiles combi: invalid setups
        ans = math.comb(k ** 2, 2)
        ans -= (k - 1) * (k - 2) * 2 * 2
        print(ans)

if __name__ == "__main__":
    solve()
