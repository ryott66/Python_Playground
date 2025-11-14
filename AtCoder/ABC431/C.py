def main() -> None:
    n, m, k = map(int, input().split())
    h = list(map(int, input().split()))
    b = list(map(int, input().split()))
    sorted_h = sorted(h)[:k]
    sorted_b = sorted(b)[m - k:]
    for i in range(k):
        if sorted_h[i] > sorted_b[i]:
            print("No")
            return
    print("Yes")

if __name__ == "__main__":
    main()
