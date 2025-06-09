n=int(input())
a=list(map(int,input().split()))
total=0
add = sum(a)

for i in range(n):
    add-= a[i]
    total+= (a[i]*add)

print(total)