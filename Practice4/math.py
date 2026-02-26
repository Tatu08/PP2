import math
import random
from typing import List

def circle_area(r: float) -> float:
    return math.pi * r * r

def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = int(math.isqrt(n))
    for d in range(3, limit + 1, 2):
        if n % d == 0:
            return False
    return True

def random_password(length: int = 10) -> str:
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))

def random_sample_stats(n: int = 10, a: int = 1, b: int = 100) -> dict:
    nums = [random.randint(a, b) for _ in range(n)]
    return {
        "numbers": nums,
        "min": min(nums),
        "max": max(nums),
        "avg": sum(nums) / len(nums)
    }

if __name__ == "__main__":
    print("circle_area(3):", round(circle_area(3), 3))
    print("distance_2d(0,0,3,4):", distance_2d(0, 0, 3, 4))
    print("is_prime(29):", is_prime(29))
    print("password:", random_password(12))
    print("sample stats:", random_sample_stats(8, 10, 50))