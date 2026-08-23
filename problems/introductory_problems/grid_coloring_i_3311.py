def solve():
    n, m = map(int, input().split())
    G = list()
    for _ in range(n):
        row = list(input())
        G.append(row)
    C = {"A", "B", "C", "D"}

    for i in range(n):
        for j in range(m):
            S = {G[i][j]}
            if i > 0: S.add(G[i - 1][j])
            if j > 0: S.add(G[i][j - 1])
            G[i][j] = list(C - S)[0]

    for row in G:
        print("".join(row))


if __name__ == "__main__":
    solve()
