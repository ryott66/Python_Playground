r,x=map(int,input().split())

# これはひどいコード　正解だからいいや

if(r<1200):
    print("No")
elif(r<1600):
    if(x==1):
        print("No")
    else:
        print("Yes")
elif(r<2400):
    print("Yes")
elif(r<3000):
    if(x==1):
        print("Yes")
    else:
        print("No")
else:
    print("No")
    
