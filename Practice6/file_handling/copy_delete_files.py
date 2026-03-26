import shutil
import os

shutil.copy("example.txt", "copy_example.txt")

if os.path.exists("copy_example.txt"):
    os.remove("copy_example.txt")
    print("File deleted")