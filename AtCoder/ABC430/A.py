def main():
    a, b, c, d = map(int, input().split())
    if a <= c and b > d:
        print("Yes")
    else:
        print("No")
    return

if __name__ == "__main__":
    main()
