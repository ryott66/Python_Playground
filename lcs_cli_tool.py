# make Longest Common Subsequence (LCS) table
def lcs_table(s1, s2):
    x = len(s1)
    y = len(s2)
    dp = [[0] * (y + 1) for _ in range(x + 1)]  # init table

    # DP
    for i in range(1, x + 1):
        for j in range(1, y + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp



# get all LCS
def find_all_lcs(dp, s1, s2, i, j, memo):
    if i == 0 or j == 0:
        return set([""])

    key = (i, j)
    if key in memo:  # already done
        return memo[key] # type dict

    if s1[i - 1] == s2[j - 1]:
        prev = find_all_lcs(dp, s1, s2, i - 1, j - 1, memo)
        result = set([s + s1[i - 1] for s in prev])
    else:
        result = set()
        if dp[i - 1][j] >= dp[i][j - 1]:  # up
            result.update(find_all_lcs(dp, s1, s2, i - 1, j, memo))
        if dp[i][j - 1] >= dp[i - 1][j]:  # left
            result.update(find_all_lcs(dp, s1, s2, i, j - 1, memo))

    memo[key] = result
    return result


# ask yes or no
def ask_yes_no():
    while True:
        yn = input("1：はい, 2：いいえ > ")

        if yn == "1":
            return True
        elif yn == "2":
            return False
        else:
            print("⚠ エラー：1（はい）または 2（いいえ）を入力してください。")



def main():
    print("最長共通部分列の長さを表示します！\n")

    while True:
        str1 = input("1つ目の文字列を入力してください：")
        str2 = input("2つ目の文字列を入力してください：")
        print("この文字列で実行しますか？")
        if ask_yes_no():
            break

    dp = lcs_table(str1, str2)
    lcs_len = dp[len(str1)][len(str2)]

    print(f"\n最長共通部分列の長さは {lcs_len} です。")

    # if get all LCS content
    print("\n最長共通部分列を表示しますか？")
    if ask_yes_no():
        memo = {}
        all_lcs = find_all_lcs(dp, str1, str2, len(str1), len(str2), memo)
        all_lcs = sorted(list(all_lcs))

        print(f"\n最長共通部分列は {len(all_lcs)} 通りあります：")
        for lcs in all_lcs:
            print(f"  - {lcs}")
    else:
        return


if __name__ == "__main__":
    main()
