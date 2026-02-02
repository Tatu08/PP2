n=int(input())
m=list(map(int,input().split()))
mx_count=0
ans=m[0]
for i in range(n):
  count=0
  for j in range(n):
    if m[i]==m[j]:
      count+=1
  if count>mx_count or (count==mx_count and m[i] < ans):
    mx_count=count
    ans=m[i]
print(ans)