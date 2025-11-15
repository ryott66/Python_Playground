n, m = map(int, input().split())

color_grid = []
for _ in range(n):
    color_grid.append(input())
# print(color_grid)
ans_grid_set = set()

for bi in range(n - m + 1):
    for bj in range(n - m + 1):
        ans_grid = []
        for k in range(m):
            ans_grid.append(color_grid[bi + k][bj : bj + m])
        ans_grid_set.add(tuple(ans_grid))

print(len(ans_grid_set))
