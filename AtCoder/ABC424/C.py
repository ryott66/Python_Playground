from collections import defaultdict
def main():
    n = int(input())
    have = [False] * (n+1)
    stack = []
    data = defaultdict(list)
    for i in range(1, n+1):
        skill = tuple(map(int, input().split()))
        data[skill[0]].append(i)
        data[skill[1]].append(i)

        if skill == (0, 0):
            have[i] = True
            stack.append(i)

    while stack:
        skill = stack.pop()
        for s in data[skill]:
            if have[s]:
                continue
            else:
                have[s] = True
                stack.append(s)

    print(sum(have))


if __name__ == '__main__':
    main()
