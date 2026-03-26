import os

os.makedirs("test_dir/sub_dir", exist_ok=True)

for item in os.listdir("test_dir"):
    print(item)