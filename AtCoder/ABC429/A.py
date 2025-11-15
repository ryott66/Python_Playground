def main():
    n,m = map(int, input().split())
    for i in range(n):
        if i < m:
            print("OK")
        else:
            print("Too Many Requests")


if __name__ == "__main__":
    main()
