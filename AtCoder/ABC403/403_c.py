n,m,q=map(int,input().split())
query=[]
for i in range(q):
    query.append(list(map(int,input().split())))

view=[set() for _ in range(n)]
allflag=[False for _ in range(n)]

for i in range(q):
    if query[i][0]==1:
        #XにYを付与
        view[query[i][1]-1].add(query[i][2])
    elif query[i][0]==2:
        #Xにすべて付与
        allflag[query[i][1] - 1] = True
    else:
        #XがY見れるか答える
        if (allflag[query[i][1]-1]==True) or (query[i][2] in view[query[i][1]-1]):
            print("Yes")
        else:
            print("No")


