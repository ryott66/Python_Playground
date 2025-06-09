#348問題C
n=int(input())
x=[]
for i in range(n):
  x.append(list(map(int,input().split())))

colorl=[]
for i in range(n):
  if x[i][1] not in colorl:
    colorl.append(x[i][1])
  else:

    pass
minlist=[]
for c in colorl:
  min=1000000
  for i in range(n):
    if x[i][1]==c:
      if min>x[i][0]:
        min=x[i][0]
  minlist.append(min)

print(max(minlist))