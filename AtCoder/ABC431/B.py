def main() -> None:
    x, n = int(input()), int(input())
    w = list(map(int, input().split()))
    data = [0] * n
    q = int(input())
    for _ in range(q):
        p = int(input())
        if data[p-1]:
            x -= w[p-1]
            data[p-1] = False
        else:
            x += w[p-1]
            data[p-1] = True
        print(x)
    return


if __name__ == "__main__":
    main()
