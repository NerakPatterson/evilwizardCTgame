import random
from classes import Character

class EvilWizard(Character):
    def __init__(self, name="Dark Wizard"):
        super().__init__(name, health=220, attack_power=50)

        # Core stats
        self.accuracy = 80
        self.crit_chance = 10
        self.defense = 8
        self.evasion = 5

        # Healing & regeneration
        self.healing_cost = 65
        self.regen_active = False

        # Cooldowns
        self.cooldowns = {
            "Dark Bolt": 0,
            "Infernal Blast": 0,
            "Mind Spike": 0,
            "Soul Drain": 0,
            "Mana Drain": 0,
            "Shadow Bind": 0,
        }

        self.last_move = None
        self.battle_log = []

        # comments
        self.random_comments = [
            "You smell like hope. I hate hope.",
            "I really hope nobody saw that.",
            "Hope is for weak and optimism for the ignorant.",
            "Did anyone bring snacks?",
            "I could do this all day… probably.",
            "I swear, I’m the best at this...",
            "Your soul looks delicious. Shame it’s attached to such a disappointing body.",
            "Your bravery is admirable. Your intelligence? Less so.",
            "I was bored. Then you showed up. Now I’m bored and annoyed.",
        ]

    def display_stats(self):
        print(f"\n{self.name}'s Stats:")
        print(f" Health: {self.health}/{self.max_health}")
        print(f" Attack Power: {self.attack_power}")
        print(f" Defense: {self.defense}")
        print(f" Accuracy: {self.accuracy}")
        print(f" Crit Chance: {self.crit_chance}")
        print(f" Evasion: {self.evasion}")

    def reduce_cooldowns(self):
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def regenerate(self):
        if self.regen_active:
            regen = random.randint(10, 20)
            self.health = min(self.health + regen, self.max_health)
            regen_msg = f"{self.name} regains {regen} HP with a flourish of glee!"
            print(regen_msg)
            self.battle_log.append(regen_msg)
            self.regen_active = False

    def take_turn(self, opponent):
        self.reduce_cooldowns()
        self.regenerate()

        if self.health <= self.max_health * 0.4 and self.cooldowns.get("Soul Drain", 0) == 0:
            chosen_move = "heal"
        else:
            chosen_move = random.choice(["attack", "special"])

        turn_msg = f"\n{self.name} twirls his cane dramatically and prepares to strike..."
        print(turn_msg)
        self.battle_log.append(turn_msg)

        if chosen_move == "attack":
            self.attack(opponent)
        elif chosen_move == "special":
            self.special_ability(opponent)
        elif chosen_move == "heal":
            self.heal()

    def attack(self, opponent):
        attacks = [
            {"key": "Dark Bolt", "multiplier": 1.0, "accuracy": 90, "crit": 10,
             "flavor": ["Mwahaha! Shadows come alive!", "Feel the sweet embrace of death!"]},
            
            {"key": "Infernal Blast", "multiplier": 1.2, "accuracy": 75, "crit": 20,
             "flavor": ["Burn, burn, burn! Such delightful chaos!", "Feel the fire from the darkest depths!"]},
            
            {"key": "Mind Spike", "multiplier": 1.5, "accuracy": 65, "crit": 30,
             "flavor": ["Mind Crush!", "Echoes of your fear amuse me!"]}
        ]
        self._execute_auto_move(attacks, opponent)

    def special_ability(self, opponent):
        abilities = [
            {"key": "Soul Drain", "multiplier": 1.8, "accuracy": 85, "crit": 15, "effect": "heal",
             "flavor": ["Your soul is mine!", "Mmm, the sweet taste of vitality!"]},
            
            {"key": "Mana Drain", "multiplier": 1.2, "accuracy": 80, "crit": 10, "effect": "regen",
             "flavor": ["The universe bends to my will!", "I drain your very essence!"]},
            
            {"key": "Shadow Bind", "multiplier": 0.6, "accuracy": 70, "crit": 5, "effect": "weaken",
             "flavor": ["You shall not escape!", "The shadows mock your futile resistance!"]}
        ]
        self._execute_auto_move(abilities, opponent)

    def heal(self):
        heal_amount = random.randint(20, 40)
        self.health = min(self.health + heal_amount, self.max_health)
        heal_msg = f"{self.name} casts a dark restorative spell and heals {heal_amount} HP!"
        print(heal_msg)
        self.battle_log.append(heal_msg)
        self.cooldowns["Soul Drain"] = 3

    def _execute_auto_move(self, moves, opponent):
        available_moves = [m for m in moves if self.cooldowns.get(m["key"], 0) == 0]
        if not available_moves:
            available_moves = moves

        chosen = random.choice(available_moves)
        key = chosen["key"]

        preview = f"{self.name} prepares to cast {key}: {random.choice(chosen.get('flavor', ['Magic happens.']))}"
        print(preview)
        self.battle_log.append(preview)

        net_hit = max(chosen["accuracy"] - getattr(opponent, "evasion", 0), 5)
        if random.randint(1, 100) > net_hit:
            miss_msg = f"{self.name} casts {key}, but it fizzles into nothing like your sex life!"
            print(miss_msg)
            self.battle_log.append(miss_msg)
            self.cooldowns[key] = 1
            return

        base = random.randint(int(self.attack_power * chosen["multiplier"] * 0.8),
                              int(self.attack_power * chosen["multiplier"] * 1.2))
        crit = random.randint(1, 100) <= chosen.get("crit", 0)
        if crit:
            base *= 2
            crit_msg = " CRITICAL!"
        else:
            crit_msg = ""

        damage = max(int(base) - getattr(opponent, "defense", 0), 0)
        opponent.health = max(opponent.health - damage, 0)

        print(f"{self.name} casts {key}!{crit_msg}")
        print(f"{opponent.name} takes {damage} damage. ({opponent.health} HP left)")
        self.battle_log.append(f"{self.name} used {key} on {opponent.name} for {damage} damage" + (" (CRIT)" if crit else ""))

        if chosen.get("effect") == "heal":
            heal_amount = damage * 0.5
            self.health = min(self.health + heal_amount, self.max_health)
            print(f"{self.name} siphons life and heals for {heal_amount:.1f} HP!")
            self.battle_log.append(f"{self.name} healed for {heal_amount:.1f} HP via Soul Drain.")
        elif chosen.get("effect") == "regen":
            self.regen_active = True
            print(f"{self.name} will regenerate health next turn!")
            self.battle_log.append(f"{self.name} activated regeneration via Mana Drain.")
        elif chosen.get("effect") == "weaken":
            if hasattr(opponent, "attack_power"):
                if not hasattr(opponent, "active_debuffs"):
                    opponent.active_debuffs = {}
                opponent.active_debuffs["attack_power"] = {"amount": 5, "duration": 2}
                print(f"{opponent.name}'s attack power is reduced by 5 for 2 turns!")
                self.battle_log.append(f"{opponent.name}'s attack power weakened by Shadow Bind.")

        self.cooldowns[key] = chosen.get("cooldown", 2)

        if opponent.health <= 0:
            msg = f"{opponent.name} has been defeated!"
            print(msg)
            self.battle_log.append(msg)
