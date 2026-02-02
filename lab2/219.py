n=int(input())
cnt={}
for i in range(n):
  s,k=input().split()
  k=int(k)
  if s in cnt:
    cnt[s]+=k
  else:
    cnt[s]=k
for name in sorted(cnt):
  print(name,cnt[name])