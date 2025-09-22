import random
from classes import Character

class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power=32)
        self.healing_cost = 65
        self.regen_active = False

        # Core stats
        self.accuracy = 80         # Base accuracy (used for fallback)
        self.crit_chance = 10      # Base crit chance
        self.defense = 8           # Reduces incoming damage
        self.evasion = 5           # EvilWizard: low

    def take_turn(self, opponent):
        actions = ["attack", "special", "heal"]
        chosen = random.choice(actions)

        print(f"\n{self.name} prepares to act...")

        if chosen == "attack":
            self.attack(opponent)
        elif chosen == "special":
            self.special_ability(opponent)
        elif chosen == "heal":
            if self.gold >= self.healing_cost and self.health < self.max_health and self.heal_cooldown == 0:
                self.heal()
            else:
                print(f"{self.name} tries to heal but fails — switching to attack instead.")
                self.attack(opponent)

    def attack(self, opponent):
        attacks = [
            {
                "name": "Dark Bolt",
                "description": "A crackling surge of shadow energy.",
                "multiplier": 1.0,
                "accuracy": 90,
                "crit": 10
            },
            {
                "name": "Infernal Blast",
                "description": "Explodes with chaotic fire.",
                "multiplier": 1.2,
                "accuracy": 75,
                "crit": 20
            },
            {
                "name": "Mind Spike",
                "description": "Pierces the mind with psychic agony.",
                "multiplier": 1.5,
                "accuracy": 65,
                "crit": 30
            }
        ]

        chosen = random.choice(attacks)

        # Evasion-based accuracy check
        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            print(f"{self.name} casts {chosen['name']} but misses!")
            return

        # Base damage
        base = random.randint(int(self.attack_power * chosen["multiplier"] * 0.8),
                              int(self.attack_power * chosen["multiplier"] * 1.2))

        # Critical hit
        if random.randint(1, 100) <= chosen["crit"]:
            base *= 2
            print(" Critical hit!")

        # Apply defense
        damage = max(base - opponent.defense, 0)
        opponent.health -= damage
        opponent.health = max(opponent.health, 0)

        print(f"{self.name} casts {chosen['name']} — {chosen['description']}")
        print(f"{opponent.name} takes {damage} damage!")
        print(f"{opponent.name} now has {opponent.health} HP remaining.")
        
    def display_stats(self):
        print(f"\n {self.name}'s Stats:")
        print(f" Health: {self.health}/{self.max_health}")
        print(f" Gold: {self.gold}")
        print(f" Defense: {self.defense}")
        print(f" Accuracy: {self.accuracy}")
        print(f" Crit Chance: {self.crit_chance}")
        print(f" Evasion: {self.evasion}")
        print(f" Regen Active: {'Yes' if self.regen_active else 'No'}")


    def special_ability(self, opponent):
        abilities = [
            {
                "name": "Soul Drain",
                "description": "Drains the opponent's life force, dealing damage and healing the caster.",
                "damage_multiplier": 1.8,
                "heal_ratio": 0.5,
                "effect": "heal",
                "accuracy": 85,
                "crit": 15
            },
            {
                "name": "Mana Drain",
                "description": "Cuts off mana resources and infects the opponent, triggering regeneration next turn.",
                "damage_multiplier": 1.2,
                "effect": "regen",
                "accuracy": 80,
                "crit": 10
            },
            {
                "name": "Shadow Bind",
                "description": "Binds the opponent in magical shadows, reducing their attack power.",
                "damage_multiplier": 0.6,
                "effect": "weaken",
                "accuracy": 70,
                "crit": 5
            }
        ]

        chosen = random.choice(abilities)

        # Evasion-based accuracy check
        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            print(f"{self.name} tries to use {chosen['name']} but it fizzles out!")
            return

        # Base damage
        base = self.attack_power * chosen["damage_multiplier"]
        base = random.randint(int(base * 0.8), int(base * 1.2))

        # Critical hit
        if random.randint(1, 100) <= chosen["crit"]:
            base *= 2
            print(" Critical effect!")

        # Apply defense
        damage = max(int(base) - opponent.defense, 0)
        opponent.health -= damage
        opponent.health = max(opponent.health, 0)

        print(f"{self.name} uses {chosen['name']} — {chosen['description']}")
        print(f"{opponent.name} takes {damage} damage!")

        if chosen["effect"] == "heal":
            heal_amount = damage * chosen["heal_ratio"]
            self.health = min(self.health + heal_amount, self.max_health)
            print(f"{self.name} heals for {heal_amount:.1f} HP!")

        elif chosen["effect"] == "regen":
            self.regen_active = True
            print(f"{self.name} will regenerate health next turn.")

        elif chosen["effect"] == "weaken":
            if hasattr(opponent, 'attack_power'):
                original_power = opponent.attack_power
                opponent.attack_power = max(opponent.attack_power * 0.7, 1)
                print(f"{opponent.name}'s attack power drops from {original_power} to {opponent.attack_power:.1f}!")

    def regenerate(self):
        if self.regen_active:
            regen = random.randint(10, 20)
            self.health = min(self.health + regen, self.max_health)
            print(f"{self.name} regenerates {regen} HP!")
            self.regen_active = False
