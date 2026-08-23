from collections import defaultdict


def solve():
    S = input()
    n = len(S)
    D = defaultdict(int)
    for c in S:
        D[c] += 1
    A = sorted(D.keys())
    m = len(A)

    arr = list()
    string = list()
    def dfs(i):
        if not D[A[i]]:
            return
        string.append(A[i])
        D[A[i]] -= 1
        if len(string) == n:
            arr.append("".join(string))
        else:
            for j in range(m):
                dfs(j)
        string.pop()
        D[A[i]] += 1

    for j in range(m):
        dfs(j)

    print(len(arr))
    for ans in arr:
        print(ans)


if __name__ == "__main__":
    solve()
