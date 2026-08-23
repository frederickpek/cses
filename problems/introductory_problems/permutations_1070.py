import sys
input = sys.stdin.readline


def main():
    n = int(input())
    if n in {2, 3}:
        print("NO SOLUTION")
        return
    A = [0] * n
    for i in range(1, n + 1):
        if i % 2 == 0:
            idx = i // 2 - 1
        else:
            idx = (n + i - 1) // 2
        A[idx] = str(i)
    print(" ".join(A))


if __name__ == "__main__":
    main()
