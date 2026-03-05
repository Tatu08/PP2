import re

S = input()
P = input()

if re.search(re.escape(P), S):
    print("Yes")
else:
    print("No")