n=int(input())
m=[]
for i in range(n):
  m.append(input())
seen=[]
res=[]
for i in range(n):
  if m[i] not in seen:
    seen.append(m[i])
    res.append((m[i],i+1))
res.sort()
for s,ind in res:
  print(s,ind)