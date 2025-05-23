#強磁性体における電子スピンの交換相互作用による規則配列シミュレーション


import random
import math
import matplotlib.pyplot as plt
import numpy as np

def change(dt:list,i:int,j:int,sita:int)->bool:  #変化後でエネルギー低ければTrue
  a=0 #元のエネルギー
  b=0 #後のエネルギー
  x=[]

  if i!=0:
    x.append(dt[j][i-1])
  if i!=4:
    x.append(dt[j][i+1])
  if j!=0:
    x.append(dt[j-1][i])
  if j!=4:
    x.append(dt[j+1][i])

  for n in x:
    deg=dt[j][i]-n
    a+=math.cos(math.radians(deg))  #aは内積の和　エネルギーは-2*Jex*内積 だからa,bは大きいほうがいい

  for n in x:
    deg=sita-n
    b+=math.cos(math.radians(deg))

  if b>=a:
    return True
  else:
    return False



def printarray(dt:list):

  #数列表示
  for i in dt:
    for j in i:
      print("{: ^5}".format(j),end="")
    print("\n")
  print("\n")


  #矢印表示
  a=np.arange(0,11,2)
  plt.xlim(0,10)
  plt.ylim(0,10)
  plt.hlines(a,0,10)
  plt.vlines(a,0,10)

  for i in range(0,5):
    for j in range(0,5):
      sita=dt[j][i] * (np.pi) / 180
      u=np.cos(sita)
      v=np.sin(sita)
      x=2*j+1
      y=2*(4-i)+1
      plt.quiver(x,y,u,v,scale_units='xy',scale=1)

  plt.axis("off")
  plt.show()
  print("\n\n")



"""----------------   main  ----------------------------"""


#5*5乱数配列作成
data=[[random.randint(0,359) for i in range(5)] for j in range(5)]
print("初期状態:\n")
printarray(data)


#200回繰り返しを5回
for y in range(5):
 for x in range(200):
  i=random.randint(0,4)
  j=random.randint(0,4)
  sita=random.randint(0,359)

  if change(data,i,j,sita):   #変化がTrueならば
    data[j][i]=sita

 print("さらに200回繰り返し後:\n")
 printarray(data)



#2000回繰り返しを3回
for y in range(3):
 for x in range(2000):
  i=random.randint(0,4)
  j=random.randint(0,4)
  sita=random.randint(0,359)

  if change(data,i,j,sita):   #変化がTrueならば
    data[j][i]=sita

 print("さらに2000回繰り返し後:\n")
 printarray(data)


 #50000回繰り返し
for x in range(50000):
  i=random.randint(0,4)
  j=random.randint(0,4)
  sita=random.randint(0,359)

  if change(data,i,j,sita):   #変化がTrueならば
    data[j][i]=sita

print("さらに50000回繰り返し後:\n")
printarray(data)