import random
from classes import Character
from heal import heal as universal_heal

class DemonSorcerer(Character):
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=40)
        self.healing_cost = 70

    def special_ability(self, opponent):
        print("\nAbilities:")
        print("1. Chaos Bolt")
        print("2. Soul Burn")
        action = input("Choose your ability: ")

        if action == "1":
            '''
            Ability:
            Description: 
            '''
            damage = random.randint(20, 60)
            opponent.health -= damage
            print(f"{self.name} hurls a Chaos Bolt at {opponent.name} for {damage} damage!")
        elif action == "2":
            '''
            Ability:
            Description: 
            '''
            damage = self.attack_power * 1.5
            opponent.health -= damage
            self.health -= 10
            print(f"{self.name} burns {opponent.name}'s soul for {damage} damage, but loses 10 HP in recoil!")