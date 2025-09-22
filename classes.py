import random

# ====================== CHARACTER CREATION ============================
def create_character():
    name = input("Enter your character's name: ")
    return Character(name, health=100, attack_power=20)

# ====================== BASE CHARACTER CLASS ============================
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health
        self.gold = 1000
        self.heal_cooldown = 0

    def attack(self, opponent):
        damage = random.randint(int(self.attack_power * 0.8), int(self.attack_power * 1.2))
        opponent.health -= damage
        opponent.health = max(opponent.health, 0)
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")

    def display_stats(self):
        print(f"{self.name} - HP: {self.health}/{self.max_health} | Gold: {self.gold}")

    def heal(self):
        heal_cost = getattr(self, 'healing_cost', 50)

        if self.gold < heal_cost:
            print(f"{self.name} doesn't have enough gold to heal! ({self.gold} gold available, {heal_cost} required)")
            return

        if self.heal_cooldown > 0:
            print(f"{self.name} can't heal yet! {self.heal_cooldown} turns remaining.")
            return

        heal_amount = random.randint(10, 20)
        self.health = min(self.health + heal_amount, self.max_health)
        self.gold -= heal_cost
        self.heal_cooldown = 3

        print(f"{self.name} heals for {heal_amount} HP at the cost of {heal_cost} gold.")
        print(f"Current health: {self.health}/{self.max_health} | Gold remaining: {self.gold}")

    def reduce_cooldowns(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1

# ====================== ENEMY CLASS ============================
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power=32)
        self.healing_cost = 65
        self.regen_active = False

    def special_ability(self, opponent):
        print("\nAbilities:")
        print("1. Soul Drain")
        print("2. Arcane Rot")
        action = input("Choose your ability: ")

        if action == "1":
            damage = self.attack_power * 1.8
            opponent.health -= damage
            self.health = min(self.health + damage * 0.5, self.max_health)
            print(f"{self.name} drains {damage} HP from {opponent.name}, healing for {damage * 0.5}!")
        elif action == "2":
            damage = self.attack_power * 1.2
            opponent.health -= damage
            self.regen_active = True
            print(f"{self.name} infects {opponent.name} with Arcane Rot for {damage} damage!")
            print(f"{self.name} will regenerate health next turn.")

    def regenerate(self):
        if self.regen_active:
            regen = random.randint(10, 20)
            self.health = min(self.health + regen, self.max_health)
            print(f"{self.name} regenerates {regen} HP from Arcane Rot!")
            self.regen_active = False

# ========================= SUBCLASSES ===================================
class ImpAssassin(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=30)
        self.healing_cost = 55
        self.evade_next = False

    def special_ability(self, opponent):
        print("\nAbilities:")
        print("1. Shadow Pierce")
        print("2. Vanish")
        action = input("Choose your ability: ")

        if action == "1":
            damage = self.attack_power * 2.3
            opponent.health -= damage
            print(f"{self.name} pierces {opponent.name} from the shadows of hell for {damage} damage!")
        elif action == "2":
            self.evade_next = True
            print(f"{self.name} vanishes into smoke — the next attack will miss!")

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
            damage = self.attack_power * 2.0
            opponent.health -= damage
            print(f"{self.name} bites {opponent.name} in a frenzy for {damage} damage!")
        elif action == "2":
            damage = self.attack_power + random.randint(10, 20)
            opponent.health -= damage
            self.health -= 5
            print(f"{self.name} howls with fury, dealing {damage} damage but losing 5 HP in recoil!")

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
            damage = random.randint(20, 60)
            opponent.health -= damage
            print(f"{self.name} hurls a Chaos Bolt at {opponent.name} for {damage} damage!")
        elif action == "2":
            damage = self.attack_power * 1.5
            opponent.health -= damage
            self.health -= 10
            print(f"{self.name} burns {opponent.name}'s soul for {damage} damage, but loses 10 HP in recoil!")

class RedemptionCleric(Character):
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
            heal_amount = random.randint(15, 30)
            self.health = min(self.health + heal_amount, self.max_health)
            print(f"{self.name} channels Holy Light and heals for {heal_amount} HP!")
        elif action == "2":
            self.shield_active = True
            print(f"{self.name} activates Divine Shield and will block the next attack!")

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
            damage = self.attack_power * 2.2
            opponent.health -= damage
            print(f"{self.name} delivers a Kiss of Pain to {opponent.name}, dealing {damage} damage!")
        elif action == "2":
            stolen_gold = random.randint(50, 150)
            opponent.gold -= stolen_gold
            self.gold += stolen_gold
            print(f"{self.name} seduces {opponent.name} and steals {stolen_gold} gold!")
