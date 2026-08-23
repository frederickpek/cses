import sys
input = sys.stdin.readline


def solve():
    A, B = sorted(map(int, input().split()))
    if B > 2 * A or (B + A) % 3:
        return print("NO")
    print("YES")

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
