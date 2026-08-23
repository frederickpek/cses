def solve():
    n = int(input())
    for i in range(1 << n):
        x = (i >> 1) ^ i
        print(f"{x:0{n}b}")

if __name__ == "__main__":
    solve()
