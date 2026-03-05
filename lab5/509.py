import re

s = input()

words = re.findall(r"\b[A-Za-z]{3}\b", s)

print(len(words))