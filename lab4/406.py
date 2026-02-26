def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

n = int(input())

first = True
for x in fibonacci(n):
    if not first:
        print(",", end="")
    print(x, end="")
    first = False