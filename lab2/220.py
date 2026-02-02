import sys
input = sys.stdin.readline
n=int(input())
doc={}
for i in range(n):
  parts=input().split()
  if parts[0]=="set":
    key=parts[1]
    value=parts[2]
    doc[key]=value
  else:
    key=parts[1]
    if key in doc:
      print(doc[key])
    else:
      print("KE: no key ",parts[1]," found in the document")