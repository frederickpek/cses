import sys

def main():
    input_data = sys.stdin.read().split()
    iterator = iter(input_data)
    n = int(next(iterator))
    A = [int(next(iterator)) for _ in range(n)]
    A.sort()
    prev = -1
    ans = 0
    for x in A:
        if x != prev:
            ans += 1
        prev = x
    print(ans)

if __name__ == "__main__":
    main()
