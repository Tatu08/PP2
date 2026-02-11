class Circle:
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r * self.r
n = int(input())
c = Circle(n)
print(f"{c.area():.2f}")
