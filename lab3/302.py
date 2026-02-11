def isUsual(a):
  while a%2==0:
    a//=2
  while a%3==0:
    a//=3
  while a%5==0:
    a//=5
  return a==1
n=int(input())
if isUsual(n):
  print("Yes")
else:
  print("No")