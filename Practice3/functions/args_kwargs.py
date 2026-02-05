def show_info(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)
show_info(1, 2, 3, name="Alice", age=20)