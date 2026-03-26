names = ["Ali", "Aruzhan", "Dias"]
scores = [85, 90, 78]

for index, name in enumerate(names):
    print(index, name)

for name, score in zip(names, scores):
    print(name, score)

x = "123"

if isinstance(x, str):
    x = int(x)

print(type(x))