"""
    dp[n]: number of ways to construct n with {1, 2, 3, 4, 5, 6}
    dp[n] = sum(dp[n - i] for i in {1, 2, 3, 4, 5, 6}: representing dp[n - i] then rolling i)
    let dp[0] = 1 -> represents future combinations with single die answers
"""

MOD = 1e9 + 7
DIE = {1, 2, 3, 4, 5, 6}

def solve():
    n = int(input())
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = sum(list(dp[i - j] for j in DIE if (i - j >= 0)))
        dp[i] = dp[i] % MOD
    print(int(dp[n]))


if __name__ == "__main__":
    solve()
