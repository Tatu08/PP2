class Father:
    def skill(self):
        print("Driving")
class Mother:
    def hobby(self):
        print("Cooking")
class Child(Father, Mother):
    pass
child = Child()
child.skill()
child.hobby()