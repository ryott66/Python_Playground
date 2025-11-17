def main():
    N = int(input())
    A = 1
    S = 0

    for _ in range(N):
        S += f(A)
        A = S

    print(A)

def f(x):
    return sum(map(int, str(x)))

# def f(n):
#     if n == 100:
#         return 1
#     return (n % 10) + (n // 10)

if __name__ == "__main__":
    main()
