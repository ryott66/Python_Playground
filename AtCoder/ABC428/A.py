def main():
    s, a, b, x = map(int, input().split())
    ans = 0
    for t in range(1, x+1):
        if t % (a + b) <= a and t % (a + b) != 0:
            ans += s
        else:
            pass
    print(ans)


if __name__ == "__main__":
    main()
