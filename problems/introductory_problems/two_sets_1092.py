import sys
input = sys.stdin.readline


def solve():
    """
        assume previous 1 to z inclusive is divisible into 2 sets A and B
        extending by 4 numbers {z + 1, z + 2, z + 3, z + 4} will also be divisible
        A U {z + 1, z + 4} and B U {z + 2, z + 3} will be the new sets
        n = 0 is divisible -> x === 0 (mod 4) are divisible
        n = 3 is divisible -> x === 3 (mod 4) are divisible
    """

    n = int(input())
    rem = n % 4
    if rem not in {0, 3}:
        print("NO")
        return

    A = list()
    B = list()
    if rem == 3:
        A.extend([1, 2])
        B.append(3)
    for i in range(0, n - 3, 4):
        A.extend([i + 1 + rem, i + 4 + rem])
        B.extend([i + 2 + rem, i + 3 + rem])

    print("YES")
    for arr in [A, B]:
        print(len(arr))
        for x in arr: print(x, end=" ")
        print()


if __name__ == "__main__":
    solve()
