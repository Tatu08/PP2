class Person:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print("Hello,", self.name)
person = Person("Alice")
person.greet()