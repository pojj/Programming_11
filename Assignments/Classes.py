# make class with specific attributes and have a shoot method
# by William

class Enemy:
    def __init__(self, health, race, attack):
        self.health = health
        self.race = race
        self.attack = attack
        
    def __str__(self):
        return ("Enemy is a "+self.race+" with "+str(self.health)+" HP and "+str(self.attack)+" attack.")
        
    def shoot(self):
        print("pew " * self.attack)
    
    
enemy1 = Enemy(100, "Banana", 10)
print(enemy1)
enemy1.shoot()

print()

enemy2 = Enemy(300, "Apple", 2)
print(enemy2)
enemy2.shoot()