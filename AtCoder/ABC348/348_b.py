#348問題B

n=int(input())
x=[]
for i in range(n):
  x.append(list(map(int,input().split())))
maxi=0
for i in range(n):
  max=0
  for j in range(n):
    if i!=j:
      d=((x[i][0]-x[j][0])**2)+((x[i][1]-x[j][1])**2)
      if max<d:
        max=d
        maxi=j+1
      else:
        pass
    else:
      pass
  print(maxi)
