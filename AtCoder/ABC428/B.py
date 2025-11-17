from collections import defaultdict

def main():
    n, k = map(int, input().split())
    s = input()
    t_freq = defaultdict(int)
    for i in range(n - k + 1):
        t_freq[s[i:i+k]] += 1

    # 汚い！簡単にkeyのmaxとれるよ。
    # max_freq = 0
    # for value in t_freq.values():
    #     if value > max_t:
    #         max_t = value
    max_freq = max(t_freq.values())
    print(max_freq)
    ans_list = []
    for key, value in t_freq.items():
        if value == max_freq:
            ans_list.append(key)

    # 汚い！.joinつかう
    # for t in sorted(ans_list):
    #     print(t, end=" ")
    print(" ".join(sorted(ans_list)))


if __name__ == "__main__":
    main()
