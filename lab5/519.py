import re

s = input()

pat = re.compile(r"\b\w+\b")
print(len(pat.findall(s)))