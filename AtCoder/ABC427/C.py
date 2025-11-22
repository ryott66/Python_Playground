# def main():    # 不正解！！！！
#     n, m = map(int, input().split())
#     node = [-1] * n
#     g = [[] for _ in range(n)]
#     for _ in range(m):
#         u, v = map(int, input().split())
#         u, v = u - 1, v - 1
#         g[u].append(v)
#         g[v].append(u)

#     ans = 0
#     for i in range(n):
#         if node[i] != -1:
#             continue
#         node[i] = 0
#         stack = [i]
#         while stack:
#             now = stack.pop()
#             for next in g[now]:
#                 if node[next] == -1:
#                     node[next] = 1 - node[now]
#                     stack.append(next)
#                 elif node[next] == node[now]:
#                     ans += 1
#     print(int(ans//2))


# ビット全探索
def main():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]

    ans = m
    for bit in range(1 << n):
        cnt = 0
        for u, v in edges:
            # u番目bitを<<で最下位ビットに持ってくる。⇒その最下位ビットを1&でとる
            if (1 & (bit >> u)) == (1 & (bit >> v)):
                cnt += 1
        ans = min(ans, cnt)
    print(ans)


if __name__ == "__main__":
    main()
