def main():
    n = int(input())
    l = list(map(int, input().split()))
    left = 0
    right = 0
    for i in range(n):
        # print("i", i)
        if l[i] == 1:
            left = i
            for j in range(n-1, left, -1):
                # print("j", j)
                if l[j] == 1:
                    right = j
                    print(right - left)
                    return
            break
    print(0)

if __name__ == "__main__":
    main()
