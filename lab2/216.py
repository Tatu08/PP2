n=int(input())
m=list(map(int,input().split()))
c=set()
for i in m:
  if i in c:
    print("NO")
  else:
    print("YES")
    c.add(i)