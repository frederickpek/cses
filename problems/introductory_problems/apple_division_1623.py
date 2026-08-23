import sys
input = sys.stdin.readline

"""
    brute force 2 ^ n
"""

class Sol:
    def __init__(self, total):
        self.total = total
        self.cumsum = 0
        self.ans = total

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    total = sum(A)
    sol = Sol(total)

    def dfs(i):
        if i == n:
            sol.ans = min(sol.ans, abs(2 * sol.cumsum - sol.total))
            return
        # pick i
        if i > -1:
            sol.cumsum += A[i]
            dfs(i + 1)
            sol.cumsum -= A[i]
        # dont pick i
        dfs(i + 1)            

    dfs(-1)
    print(sol.ans)



if __name__ == "__main__":
    solve()
