import math

R = float(input().strip())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

def dist(a, b, c, d):
    return math.hypot(c - a, d - b)

def dist_point_to_segment(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    vv = vx * vx + vy * vy
    if vv == 0:
        return math.hypot(px - ax, py - ay)
    t = (wx * vx + wy * vy) / vv
    if t < 0:
        return math.hypot(px - ax, py - ay)
    if t > 1:
        return math.hypot(px - bx, py - by)
    cx, cy = ax + t * vx, ay + t * vy
    return math.hypot(px - cx, py - cy)

AB = dist(x1, y1, x2, y2)
dseg = dist_point_to_segment(0.0, 0.0, x1, y1, x2, y2)

if dseg >= R - 1e-12:
    ans = AB
else:
    da = math.hypot(x1, y1)
    db = math.hypot(x2, y2)

    dot = x1 * x2 + y1 * y2
    cos_t = dot / (da * db)
    cos_t = max(-1.0, min(1.0, cos_t))
    theta = math.acos(cos_t)

    a = 0.0 if da <= R + 1e-12 else math.acos(R / da)
    b = 0.0 if db <= R + 1e-12 else math.acos(R / db)

    arc = theta - a - b
    if arc < 0:
        arc = 0.0

    ta = 0.0 if da <= R + 1e-12 else math.sqrt(max(0.0, da * da - R * R))
    tb = 0.0 if db <= R + 1e-12 else math.sqrt(max(0.0, db * db - R * R))

    ans = ta + tb + R * arc

print(f"{ans:.10f}")