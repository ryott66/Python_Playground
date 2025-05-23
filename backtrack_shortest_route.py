import copy

def printarray(dt:list):
  ctm=0
  for row in dt:
    for i in range(0,len(row)):
      if row[i]==8:
        row[i]="■"
      elif row[i]==0:
        row[i]=" "
      else:
        ctm+=1
        row[i]="○"
    print("".join(row))
  print("{:d}で到着\n".format(ctm))


def try_move(data:list,x:int,y:int)->bool:#返り値は真偽
  global ans
  global  move_vec
  for dx,dy in move_vec:
    x1=x+dx
    y1=y+dy

    if data[y1][x1]==0:
      data[y1][x1]=1
      if try_move(data,x1,y1)==False:  #どこもいけなくなったときFALSEが返る
        data[y1][x1]=0
     #else:NR
     #if文ではあるがtry_moveは実行されていて、再起でもしTRUE(GOAL)まで行けたら動かしたまま、つまり何もしなくていい
    elif data[y1][x1]==9:
      if data in ans:
        return False
      #↓if入ったらreturnするので実質elseのとき
      ans.append(copy.deepcopy(data))
      printarray(data)
      return True
  else: #forが途中で終わらなかったら
    return False



ans=[]
move_vec=[(0,1),(1,0),(-1,0),(0,-1)]


for i in range(0,100):#100通り以下前提
  data1=[
     [8,8,8,8,8,8,8,8,8,8],
     [8,1,0,0,8,8,0,0,0,8],
     [8,0,8,0,0,0,0,8,0,8],
     [8,0,8,8,8,0,8,8,0,8],
     [8,0,0,8,8,0,0,8,0,8],
     [8,8,0,0,8,0,8,8,0,8],
     [8,0,8,0,8,0,0,8,0,8],
     [8,0,0,0,8,8,0,0,0,8],
     [8,8,8,0,0,0,0,8,0,8],
     [8,8,8,8,8,8,8,8,9,8]
   ]
  try_move(data1,1,1)

