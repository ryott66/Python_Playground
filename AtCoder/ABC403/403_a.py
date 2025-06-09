n=int(input())
A=list(map(int,input().split()))

sum=0
for i in range(1,n+1):
    if i%2==1:
        sum+=A[i-1]
    else:
        pass
print(sum)