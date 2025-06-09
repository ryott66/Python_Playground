import sys

n, m=map(int, input().split())
a=list(map(int, input().split()))

data=[False for _ in range(m)]
ct=0

for i in range(n):

    if data[a[i]-1]==False:
        data[a[i]-1]=True
        ct+=1
        if ct==m:
            print(n-i)
            sys.exit(0)
        else:
            pass
    else:
        pass
print(0)


    