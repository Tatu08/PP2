a=int(input())
b=list(map(int,input().split()))
mx=b[0]
for x in b:
  if x > mx:
    mx=x
print(mx)