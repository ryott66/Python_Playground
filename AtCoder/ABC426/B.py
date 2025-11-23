from collections import defaultdict
def main():
    s = input()
    ch = defaultdict(int)
    for c in s:
        ch[c] += 1

    for c, ct in ch.items():
        if ct == 1:
            print(c)


if __name__ == "__main__":
    main()
