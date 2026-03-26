with open("example.txt", "w") as file:
    file.write("Hello, this is a test file.\n")

with open("example.txt", "a") as file:
    file.write("Adding new line.\n")