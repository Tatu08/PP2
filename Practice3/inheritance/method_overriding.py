class Animal:
    def speak(self):
        print("Animal speaks")
class Cat(Animal):
    def speak(self):
        print("Cat meows")
cat = Cat()
cat.speak()