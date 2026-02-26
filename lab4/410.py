def cycle_list(lst, k):
    for _ in range(k):
        for item in lst:
            yield item

lst = input().split()
k = int(input())

first = True
for x in cycle_list(lst, k):
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False