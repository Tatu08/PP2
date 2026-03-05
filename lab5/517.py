import re

s = input()

matches = re.findall(r"\d{2}/\d{2}/\d{4}", s)

print(len(matches))