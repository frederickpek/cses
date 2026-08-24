"""
let set of coin values be C
dp[i] be minimum number of coins required to reach value i
dp[i] = 1 if i in C else, min(dp[i - c] + 1 for c in C)

python TLEs
"""

def solve():
    n, T = map(int, input().split())
    C = list(map(int, input().split()))
    dp = [0] * (T + 1)
    for i in range(T + 1):
        candidates = [dp[i - c] + 1 for c in C if (i - c >= 0)]
        dp[i] = min(candidates) if candidates else 0
    print(dp[T] or -1)

if __name__ == "__main__":
    solve()
