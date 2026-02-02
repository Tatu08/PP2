n=int(input())
m=[]
for i in range(n):
  m.append(input())
cc=0  
mm=[]
for i in range(n):
  if m[i] in mm:
    continue
  count=0
  for j in range(n):
    if m[i]==m[j]:
      count+=1
  if count==3:
    cc+=1
  mm.append(m[i])
print(cc)