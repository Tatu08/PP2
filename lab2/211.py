a,b,c = map(int,input().split())
n = list(map(int, input().split()))
n[b-1:c]=n[b-1:c][::-1]
print(*n)