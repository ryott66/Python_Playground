t=input()
u=input()

for i in range(len(t)-len(u)+1):
    jadge=True
    for j in range(len(u)):
        if t[i+j]=="?" or t[i+j]==u[j]:#Yes
            pass
        else:#No
            jadge=False
            break
    if jadge==True:
        break#End

if jadge==True:
    print("Yes")
else:
    print("No")
    