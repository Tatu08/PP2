class Parent:
    def __init__(self, name):
        self.name = name
class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age
child = Child("Alice", 10)
print(child.name, child.age)