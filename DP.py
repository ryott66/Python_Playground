def solve():
    n, k = map(int, input().split())
    s = input().strip()

    m = n - 2  # 区間数

    # 各区間の gain（S の数）を計算
    gain = [0] * m
    for i in range(m):
        gain[i] = (s[i] == 'S') + (s[i+1] == 'S') + (s[i+2] == 'S')

    # dp[i][j] = 区間 i から最後まで見て j 回選ぶ時の gain max
    dp = [[0] * (k+1) for _ in range(m+3)]

    # i を後ろから前へ
    for i in range(m-1, -1, -1):
        for j in range(k+1):
            # 選ばない
            best = dp[i+1][j]

            # 選ぶ
            if j > 0:
                best = max(best, gain[i] + dp[i+3][j-1])

            dp[i][j] = best

    S_total = s.count('S')
    S_removed = min(S_total, dp[0][k])
    print(n - (S_total - S_removed))
    print(dp)

if __name__ == "__main__":
    solve()
