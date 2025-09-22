import random
from classes import Character
from heal import heal as universal_heal

class Seraphin(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=20)
        self.healing_cost = 30
        self.shield_active = False

    def special_ability(self, opponent):
        print("\nAbilities:")
        print("1. Holy Light")
        print("2. Divine Shield")
        action = input("Choose your ability: ")

        if action == "1":
            '''
            Ability:
            Description: 
            '''
            heal_amount = random.randint(15, 30)
            self.health = min(self.health + heal_amount, self.max_health)
            print(f"{self.name} channels Holy Light and heals for {heal_amount} HP!")
        elif action == "2":
            '''
            Ability:
            Description: 
            '''
            self.shield_active = True
            print(f"{self.name} activates Divine Shield and will block the next attack!")