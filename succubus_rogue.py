import random
from classes import Character
from heal import heal as universal_heal

class SuccubusRogue(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=25)
        self.healing_cost = 50

    def special_ability(self, opponent):
        print("\nAbilities:")
        print("1. Kiss of Pain")
        print("2. Seduce and Steal")
        action = input("Choose your ability: ")

        if action == "1":
            '''
            Ability:
            Description: 
            '''
            damage = self.attack_power * 2.2
            opponent.health -= damage
            print(f"{self.name} delivers a Kiss of Pain to {opponent.name}, dealing {damage} damage!")
        elif action == "2":
            '''
            Ability:
            Description: 
            '''
            stolen_gold = random.randint(50, 150)
            opponent.gold -= stolen_gold
            self.gold += stolen_gold
            print(f"{self.name} seduces {opponent.name} and steals {stolen_gold} gold!")
