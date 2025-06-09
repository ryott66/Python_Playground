from collections import deque

q=int(input())
queue=deque()
query=[]
for i in range(q):
    query=list(map(int,input().split()))
    if query[0]==1:
        queue.append(query[1])
    else:
        print(queue.popleft())
