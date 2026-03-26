import shutil

shutil.move("example.txt", "test_dir/example.txt")

shutil.copy("test_dir/example.txt", "example.txt")