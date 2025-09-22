import random
from classes import Character
from heal import heal as universal_heal

class ImpAssassin(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=30)
        self.healing_cost = 55
        self.evade_next = False
        self.last_move = None


        # Core stats
        self.accuracy = 95
        self.crit_chance = 25
        self.defense = 5
        self.speed = 30
        self.evasion = 20  # High evasion

        self.cooldowns = {
            "Shadow Strike": 0,
            "Crotch Kick": 0,
            "Blue Blood Shot": 0,
            "Jugular Slash": 0,
        }
        
    def display_stats(self):
        print(f"\n {self.name}'s Stats:")
        print(f" Health: {self.health}/{self.max_health}")
        print(f" Gold: {self.gold}")
        print(f" Defense: {self.defense}")
        print(f" Accuracy: {self.accuracy}")
        print(f" Crit Chance: {self.crit_chance}")
        print(f" Speed: {self.speed}")
        print(f" Evasion: {self.evasion}")
        
    def heal(self):
        # Set healing parameters before calling universal logic
        self.heal_amount = 25
        self.heal_cooldown_duration = 2
        universal_heal(self)


    def attack(self, opponent):
        attacks = [
            {
                "key": "Shadow Strike",
                "name": "Shadow Strike",
                "description": "A swift stab from the shadows.",
                "multiplier": 1.0,
                "accuracy": 95,
                "crit": 20,
                "cooldown": 1
            },
            {
                "key": "Crotch Kick",
                "name": "Crotch Kick",
                "description": "A ruthless low blow.",
                "multiplier": 0.7,
                "accuracy": 90,
                "crit": 10,
                "cooldown": 2
            }
        ]

        while True:
            print("\nAttack:")
            for i, move in enumerate(attacks, 1):
                print(f"{i}. {move['name']}")
            print("B. Go Back")
            action = input("Choose your attack: ")

            if action.upper() == "B":
                return

            try:
                chosen = attacks[int(action) - 1]
            except:
                print("Invalid choice. Try again.")
                continue

            key = chosen["key"]
            if self.last_move == key:
                print(f"You can't use {key} twice in a row!")
                continue
            if self.cooldowns[key] > 0:
                print(f"{key} is on cooldown for {self.cooldowns[key]} more turn(s)!")
                continue

            net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
            if random.randint(1, 100) > net_hit_chance:
                print(f"{self.name} attempts {key} but misses!")
                self.last_move = key
                self.cooldowns[key] = chosen["cooldown"]
                break

            base = random.randint(int(self.attack_power * chosen["multiplier"] * 0.8),
                                  int(self.attack_power * chosen["multiplier"] * 1.2))

            if random.randint(1, 100) <= chosen["crit"]:
                base *= 2
                print("💥 Critical hit!")

            damage = max(base - opponent.defense, 0)
            opponent.health = max(opponent.health - damage, 0)

            print(f"{self.name} uses {key} — {chosen['description']}")
            print(f"{opponent.name} takes {damage} damage and now has {opponent.health} HP remaining.")

            self.last_move = key
            self.cooldowns[key] = chosen["cooldown"]
            break

    def special_ability(self, opponent):
        abilities = [
            {
                "key": "Blue Blood Shot",
                "name": "Blue Blood Shot",
                "description": "A venomous shot that targets noble veins.",
                "multiplier": 1.5,
                "accuracy": 90,
                "crit": 25,
                "cooldown": 3
            },
            {
                "key": "Jugular Slash",
                "name": "Jugular Slash",
                "description": "A brutal slash aimed at the throat.",
                "multiplier": 3.0,
                "accuracy": 70,
                "crit": 40,
                "cooldown": 4
            }
        ]

        while True:
            print("\nAbilities:")
            for i, move in enumerate(abilities, 1):
                print(f"{i}. {move['name']}")
            print("B. Go Back")
            action = input("Choose your ability: ")

            if action.upper() == "B":
                return

            try:
                chosen = abilities[int(action) - 1]
            except:
                print("Invalid choice. Try again.")
                continue

            key = chosen["key"]
            if self.last_move == key:
                print(f"You can't use {key} twice in a row!")
                continue
            if self.cooldowns[key] > 0:
                print(f"{key} is on cooldown for {self.cooldowns[key]} more turn(s)!")
                continue

            net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
            if random.randint(1, 100) > net_hit_chance:
                print(f"{self.name} attempts {key} but misses!")
                self.last_move = key
                self.cooldowns[key] = chosen["cooldown"]
                break

            base = self.attack_power * chosen["multiplier"]
            base = random.randint(int(base * 0.8), int(base * 1.2))

            if random.randint(1, 100) <= chosen["crit"]:
                base *= 2
                print("💥 Critical hit!")

            damage = max(int(base) - opponent.defense, 0)
            opponent.health = max(opponent.health - damage, 0)

            print(f"{self.name} uses {key} — {chosen['description']}")
            print(f"{opponent.name} takes {damage} damage and now has {opponent.health} HP remaining.")

            self.last_move = key
            self.cooldowns[key] = chosen["cooldown"]
            break