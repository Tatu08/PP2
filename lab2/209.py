n = int(input())
a = list(map(int, input().split()))
mx=max(a)
mn=min(a)
for i in range(0,n):
  if a[i]==mx:
    a[i]=mn
print(*a)