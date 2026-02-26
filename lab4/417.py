import math

R = float(input().strip())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R

ans = 0.0

if a == 0:
    ans = 0.0
else:
    D = b*b - 4*a*c
    if D < 0:
        insideA = (x1*x1 + y1*y1) <= R*R
        insideB = (x2*x2 + y2*y2) <= R*R
        ans = math.hypot(dx, dy) if (insideA and insideB) else 0.0
    else:
        sqrtD = math.sqrt(D)
        t1 = (-b - sqrtD) / (2*a)
        t2 = (-b + sqrtD) / (2*a)
        if t1 > t2:
            t1, t2 = t2, t1
        L = max(t1, 0.0)
        U = min(t2, 1.0)
        ans = 0.0 if U <= L else math.hypot(dx, dy) * (U - L)

print(f"{ans:.10f}")