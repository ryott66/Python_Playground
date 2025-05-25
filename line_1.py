import sys

def main(lines):
    n, m = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    reserved_set = set(a)

    q = int(lines[2])
    queries = []
    for i in range(q):
        l, r = map(int, lines[3 + i].split())
        queries.append((l, r))

    anslist = []
    for l, r in queries:
        ans = -1
        for i in range(l, r + 1):  # rを含む範囲
            if i not in reserved_set:
                ans = i
                break
        anslist.append(ans)

    for ans in anslist:
        print(ans)

if __name__ == '__main__':
    lines = []
    lines = ["10 5", "3 4 6 7 8", "3", "1 1", "3 7", "6 8"]

    main(lines)
