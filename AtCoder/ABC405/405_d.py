from collections import deque

h,w=map(int, input().split())
s=[]

s=[list(input()) for _ in range(h)]


queue=deque()

for i in range(h):
    for j in range(w):
        if s[i][j]=="E":
            queue.append([i,j])

dall=[[-1,0,"v"],[0,1,"<"],[1,0,"^"],[0,-1,">"]]  #上右下左


while queue:
    current=queue.popleft()
    for d in dall:
        suri=current[0]+d[0]   #surround_i
        surj=current[1]+d[1]   #surround_j
        if (0 <= suri < h) and (0 <= surj < w):
            if s[suri][surj]==".":  
                s[suri][surj]=d[2]
                queue.append([suri,surj])

for i in s:
    for j in i:
        print(j, end="")
    print("")