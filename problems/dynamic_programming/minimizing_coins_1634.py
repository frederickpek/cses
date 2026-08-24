"""
let set of coin values be C
dp[i] be minimum number of coins required to reach value i
dp[i] = 1 if i in C else, min(dp[i - c] + 1 for c in C)
"""

inf = float("inf")

def solve():
    n, T = map(int, input().split())
    C = list(map(int, input().split()))
    dp = [inf] * (T + 1)
    dp[0] = 0
    for c in C:
        for i in range(T + 1):
            if i - c < 0: continue
            dp[i] = min(dp[i], dp[i - c] + 1)
    print(-1 if dp[T] == inf else dp[T])

if __name__ == "__main__":
    solve()
