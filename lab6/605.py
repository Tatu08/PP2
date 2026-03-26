s = input().lower()

vowels = "aeiou"

print("Yes" if any(c in vowels for c in s) else "No")