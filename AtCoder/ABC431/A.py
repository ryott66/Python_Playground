def main():
    h, b = map(int, input().split())
    if h > b:
        print(h - b)
        return
    print(0)

if __name__ == "__main__":
    main()
