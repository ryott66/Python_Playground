def main():
    n = int(input())
    a = list(map(int, input().split()))
    num_dict = {}
    ans = 0
    for i in range(n):
        num_dict.setdefault(a[i], []).append(i)

    for idx_list in num_dict.values():
        if len(idx_list) >= 2:
            ans += int((n - len(idx_list)) * ((len(idx_list)*(len(idx_list)-1))/2))
    print(ans)

if __name__ == "__main__":
    main()


# 結局キーもバリューも使ってないから頻度だけ入れるリストで良かった。
