def main():
    S = input()
    curr = ans = 1
    prev = S[0]
    n = len(S)
    for i in range(1, n):
        if S[i] == prev:
            curr += 1
        else:
            prev = S[i]
            curr = 1
        ans = max(ans, curr)
    print(ans)

if __name__ == "__main__":
    main()
