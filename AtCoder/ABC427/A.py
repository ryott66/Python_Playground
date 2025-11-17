def main():
    s = list(input())
    # print(s)

    c_idx = int((len(s) - 1) / 2)
    ans = s[:c_idx] + s[c_idx + 1:]
    print("".join(ans))

if __name__ == "__main__":
    main()

# =========list にする必要なかった！===================
