import random
from classes import Character
from heal import heal as universal_heal

class HellhoundBerserker(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=28)
        self.healing_cost = 45

    def special_ability(self, opponent):
        print("\nAbilities:")
        print("1. Frenzy Bite")
        print("2. Howl of Fury")
        action = input("Choose your ability: ")

        if action == "1":
            '''
            Ability:
            Description: 
            '''
            damage = self.attack_power * 2.0
            opponent.health -= damage
            print(f"{self.name} bites {opponent.name} in a frenzy for {damage} damage!")
        elif action == "2":
            '''
            Ability:
            Description: 
            '''
            damage = self.attack_power + random.randint(10, 20)
            opponent.health -= damage
            self.health -= 5
            print(f"{self.name} howls with fury, dealing {damage} damage but losing 5 HP in recoil!")

