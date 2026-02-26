
m = int(input())
g = 0
n = 0

for _ in range(m):
    scope, val = input().split()
    x = int(val)
    if scope == "global":
        g += x
    elif scope == "nonlocal":
        n += x

print(g, n)