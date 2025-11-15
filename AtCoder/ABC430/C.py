def main() -> None:
    n, a, b = map(int, input().split())
    s = input()

    sum_a = [0]* (n+1)
    sum_b = [0]* (n+1)
    for i in range(1, n+1):
        if s[i-1] == "a":
            sum_a[i] = sum_a[i-1] + 1
            sum_b[i] = sum_b[i-1]
        else:
            sum_b[i] = sum_b[i-1] + 1
            sum_a[i] = sum_a[i-1]

    Ra = 1
    Rb = 1
    ans = 0

    for l in range(1, n+1):
        while Ra <= n and sum_a[Ra] - sum_a[l-1] < a:
            Ra += 1
        while Rb <= n and sum_b[Rb] - sum_b[l-1] < b:
            Rb += 1
        if Ra > n:
            break

        ans += max(0, Rb - Ra)

    print(ans)
    return


if __name__ == "__main__":
    main()





N, A, B = map(int, input().split())
S = input()

cum_a = [0] * (N + 1)
cum_b = [0] * (N + 1)

for i in range(N):
    cum_a[i + 1] = cum_a[i] + (S[i] == 'a')
    cum_b[i + 1] = cum_b[i] + (S[i] == 'b')

ans = 0
right_a = 1
right_b = 1

for l in range(0, N + 1):
    while right_a < (N + 1) and cum_a[right_a] - cum_a[l] < A:
        right_a += 1
    while right_b < (N + 1) and cum_b[right_b] - cum_b[l] < B:
        right_b += 1
    count = max(0, right_b - right_a)
    ans += count

print(ans)

