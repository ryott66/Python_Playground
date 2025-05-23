d0 = [ 8, 14, 13, 7, 15, 12, 16, 15, 12, 9 ]

d1 = [ 8, 14, 13, 7, 15 ]

d2 = [ 8, 14, 13, 7, 15, 12, 16, 15, 12, 9, 20, 22, 15, 12, 11,
  25, 13, 7, 10, 6, 11, 11, 5, 8, 16, 7, 11, 18, 12, 9
]

d3 = [
   8, 14, 13, 7, 15, 12, 16, 15, 12, 9, 20, 22, 15, 12, 11,
   8, 14, 13, 7, 15, 12, 16, 15, 12, 9, 20, 22, 15, 12, 11,
  25, 13, 7, 10, 6, 11, 11, 5, 8, 16, 7, 11, 18, 12, 9,
  25, 13, 7, 10, 6, 11, 11, 5, 8, 16, 7, 11, 18, 12, 9,
   8, 14, 13, 7, 15, 12, 16, 15, 12, 9, 20, 22, 15, 12, 11,
  25, 13, 7, 10, 6, 11, 11, 5, 8, 16, 7, 11, 18, 12, 9,
   8, 14, 13, 7, 15, 12, 16, 15, 12, 9, 20, 22, 15, 12, 11,
   8, 14, 13, 7, 15, 12, 16, 15, 12, 9, 20, 22, 15, 12, 11,
  25, 13, 7, 10, 6, 11, 11, 5, 8, 16, 7, 11, 18, 12, 9,
  25, 13, 7, 10, 6, 11, 11, 5, 8, 16, 7, 11, 18, 12, 9
]

d4 = [
  80000, 140000, 130000, 70000, 150000, 120000, 160000, 150000, 120000, 90000, 200000, 220000, 150000, 120000, 110000,
  80000, 140000, 130000, 70000, 150000, 120000, 160000, 150000, 120000, 90000, 200000, 220000, 150000, 120000, 110000,
  250000, 130000, 70000, 100000, 60000, 110000, 110000, 50000, 80000, 160000, 70000, 110000, 180000, 120000, 90000,
  80000, 140000, 130000, 70000, 150000, 120000, 160000, 150000, 120000, 90000, 200000, 220000, 150000, 120000, 110000,
  250000, 130000, 70000, 100000, 60000, 110000, 110000, 50000, 80000, 160000, 70000, 110000, 180000, 120000, 90000,
  250000, 130000, 70000, 100000, 60000, 110000, 110000, 50000, 80000, 160000, 70000, 110000, 180000, 120000, 90000,
  80000, 140000, 130000, 70000, 150000, 120000, 160000, 150000, 120000, 90000, 200000, 220000, 150000, 120000, 110000,
  80000, 140000, 130000, 70000, 150000, 120000, 160000, 150000, 120000, 90000, 200000, 220000, 150000, 120000, 110000,
  250000, 130000, 70000, 100000, 60000, 110000, 110000, 50000, 80000, 160000, 70000, 110000, 180000, 120000, 90000,
  250000, 130000, 70000, 100000, 60000, 110000, 110000, 50000, 80000, 160000, 70000, 110000, 180000, 120000, 90000
]



import itertools
def haiti(dt:list):
  while True:
    n=int(input("見張りの人数を入力してください\n："))
    if 1<n<len(dt):
      break
    print("エラー\n")
  num=[]
  for i in range(0,len(dt)): 
    num.append(i)
  comb=list(itertools.combinations(num,n))
  sum=[0]*n
  ans=0

  for i in comb:
  #sum作成
    for x in range(0,n-1):
      for j in range(i[x],i[x+1]):
        sum[x]+=dt[j]
    #sum[n]だけは特別
    for k in range(i[n-1],len(dt)):
      sum[n-1]+=dt[k]
    for l in range(0,i[0]):
      sum[n-1]+=dt[l]
    #sumの最小が最大になってるか
    if min(sum)>ans:
      ans=min(sum)
      ansnum=i
    sum=[0]*n  #sumをリセット

  print("見張りを配置する塔は")
  for i in range(0,n):
   print("{:d}番目".format(ansnum[i]+1),end=" ")
  print("この時の塔間の距離の最小値は{:d}です。\n".format(ans))

def judge(dt:list,n:int,x:int):
  ans=0
  for i in range(0,len(dt)):#スタート地点
    for j in range(i,len(dt)):#スタートから最後の塔まで
      ans+=dt[j]
      tmp=0
      ctn=1
      if ans==x:# and x*n<sum(dt):
        for l in range(j+1,len(dt)):
          tmp+=dt[l]
          if tmp>=ans:
            tmp=0
            ctn+=1
        for l in range(0,i):
          tmp+=dt[l]
          if tmp>=ans:
            tmp=0
            ctn+=1
        if ctn>=n:
          return True
      elif ans>x:
        break
    for k in range(0,i):#最初の塔からスタートまで
      ans+=dt[k]
      if ans==x:# and x*n<sum(dt):
        for l in range(j+1,len(dt)):
          tmp+=dt[l]
          if tmp>=ans:
            tmp=0
            ctn+=1
        for l in range(0,i):
          tmp+=dt[l]
          if tmp>=ans:
            tmp=0
            ctn+=1
        if ctn>=n:
          return True
      elif ans>x:
        break
    ans=0


def linear(dt:list):
  while True:
    n=int(input("見張りの人数を入力してください\n："))
    if 1<n<=len(dt):
        break
    print("エラー\n")

  x=min(dt)
  while True:
   if judge(dt,n,x):
     kouho=x
 #    print("候補に",x)
   x+=1

   if x>(sum(dt)/n):
     break
  print("答えは",end="")
  print(kouho)



def binary(dt:list):

  while True:
    n=int(input("見張りの人数を入力してください\n："))
    if 1<n<=len(dt):
        break
    print("エラー\n")
  kouho=0
  i=0
  j=sum(dt)//n
  mitukaranai=0
  senkei=0
  while True:
    if mitukaranai==1:
      if senkei==1:
        t=k
      k+=1#見つかんなかったら条件分岐で線形探索っぽくいく
    else:
      k=(i+j)//2#「//」は商の整数値という意味

    if judge(dt,n,k):
      senkei=0
      kouho=k
      i=k+1#見つかったらそれより上を探す
   #   print("候補に",k)
      mitukaranai=0
    else:
      mitukaranai=1#見つからなかった時それより下とは限らない
      senkei+=1
    if j<=i:
      break
    if j<=k:
      j=t-1
      senkei=0
      mitukaranai=0
  print("答えは",end="")
  print(kouho)
      


haiti(d0)
haiti(d0)
haiti(d0)
haiti(d1)
haiti(d1)
haiti(d1)



linear(d2)
linear(d2)
linear(d3)
linear(d3)
# linear(d4)
# linear(d4)

binary(d3)
binary(d3)
binary(d4)
binary(d4)