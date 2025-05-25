def func1():
    name = "John"

def func2():
    name = "Vova"

func1()


name1 = "Tom"
age1 = 24
weapon1 = "Sword"

class Hero:
    def __init__(self, name, age, weapon):
        self.name = name
        self.age = age
        self.weapon =weapon

    def print_info(self):
        print("Name: ", self.name)
        print("Age: ", self.age)
        print("Weapon: ", self.weapon)


hero1 = Hero("Job", 26, "crab")
lamp1 = Lamp(True)

hero2 = Hero("Ball", 15, "sword")
hero2.print_info()
hero1.print_info()