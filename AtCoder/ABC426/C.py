import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())
    ver = [1] * (n+1)
    min_now = 1
    for _ in range(q):
        x, y = map(int, input().split())
        ans = 0
        if x < min_now:
            print(0)
            continue
        while min_now <= x:
            ans += ver[min_now]
            ver[min_now] = 0
            min_now += 1
        ver[y] += ans
        print(ans)


if __name__ == "__main__":
    main()
