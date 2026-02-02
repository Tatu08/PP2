n = int(input())
a = list(map(int, input().split()))
while n>0:
  n-=1
  a[n]*=a[n]
print(*a)