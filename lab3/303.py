s = input().strip()
to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}
to_word = {v: k for k, v in to_digit.items()}
for op in ['+', '-', '*']:
    if op in s:
        left, right = s.split(op)
        operator = op
        break
def parse_number(word):
    res = ""
    for i in range(0, len(word), 3):
        res += to_digit[word[i:i+3]]
    return int(res)
a = parse_number(left)
b = parse_number(right)
if operator == '+':
    ans = a + b
elif operator == '-':
    ans = a - b
else:
    ans = a * b
result = ""
for d in str(ans):
    result += to_word[d]
print(result)