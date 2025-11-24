def main():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    sum_prefix = [0]
    for i in range(0, n):
        sum_prefix.append(sum_prefix[i] + a[i])
    now = 0
    for _ in range(q):
        query = input()
        if query[0] == "1":
            _, c = query.split()
            c = int(c)
            now = (now + c) % n
        else:
            _, l, r = query.split()
            l = int(l); r = int(r)
            l, r = l-1, r-1
            l = (now+l) % n
            r = (now+r) % n

            if l <= r:
                ans = sum_prefix[r+1]-sum_prefix[l]
            else:
                ans = sum_prefix[n] - (sum_prefix[l]-sum_prefix[r+1])
            print(ans)

if __name__ == '__main__':
    main()
