def div_by_3_and_4(n):
    for x in range(0, n + 1):
        if x % 3 == 0 and x % 4 == 0:
            yield x

n = int(input())

first = True
for x in div_by_3_and_4(n):
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False