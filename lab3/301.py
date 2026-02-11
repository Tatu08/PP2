a=input()
b=True
for i in a:
  if int(i)%2!=0:
    b=False
    break
if b:
  print("Valid")
else:
  print("Not Valid")