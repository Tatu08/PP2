n = int(input())
nums = list(map(int, input().split()))

squares = map(lambda x: x*x, nums)

print(sum(squares))