I = lambda: map(int, input().split())


def main():
    n = int(input())
    A = list(I())
    prev = A[0]
    ans = 0
    for i in range(1, n):
        if prev > A[i]:
            ans += prev - A[i]
            continue
        prev = A[i]
    print(ans)

if __name__ == "__main__":
    main()
