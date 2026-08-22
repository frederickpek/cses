I = lambda: map(int, input().split())

def main():
    n = int(input())
    A = set(I())
    for x in range(1, n + 1):
        if x not in A:
            print(x)
            return


if __name__ == "__main__":
    main()
