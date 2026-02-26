import importlib

q = int(input())
for _ in range(q):
    mod_path, attr = input().split()

    try:
        module = importlib.import_module(mod_path)
    except Exception:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(module, attr):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    val = getattr(module, attr)
    print("CALLABLE" if callable(val) else "VALUE")