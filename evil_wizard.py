import random
from classes import Character

class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power=32)
        self.healing_cost = 65
        self.regen_active = False
        self.last_move = None
        self.battle_log = []

        # Core stats
        self.accuracy = 80
        self.crit_chance = 10
        self.defense = 8
        self.evasion = 5

        # Move cooldowns
        self.cooldowns = {
            "Dark Bolt": 0,
            "Infernal Blast": 0,
            "Mind Spike": 0,
            "Soul Drain": 0,
            "Mana Drain": 0,
            "Shadow Bind": 0,
        }

        # Flavor lines
        self.random_comments = [
            "Phrasing!",
            "I really hope nobody saw that.",
            "Did anyone bring snacks?",
            "I could do this all day… probably.",
            "I swear, I’m the best at this.",
            "Drink! I mean… spell. Yeah, spell."
        ]

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
        # Reduce cooldowns and apply regeneration if active
        self.reduce_cooldowns()
        self.regenerate()

        # Determine priority: heal if low health
        if self.health <= self.max_health * 0.4 and self.cooldowns.get("Soul Drain", 0) == 0:
            chosen_move = "heal"
        else:
            # Otherwise choose attack or special ability
            chosen_move = random.choice(["attack", "special"])

        turn_msg = f"\n{self.name} twirls his cane dramatically and prepares to act..."
        print(turn_msg)
        self.battle_log.append(turn_msg)

        if chosen_move == "attack":
            self._auto_attack(opponent)
        elif chosen_move == "special":
            self._auto_special(opponent)
        elif chosen_move == "heal":
            self._auto_heal()

    def _auto_attack(self, opponent):
        attacks = [
            {"key": "Dark Bolt", "multiplier": 1.0, "accuracy": 90, "crit": 10, 
             "flavor": ["Mwahaha! Shadows come alive!", "Observe the chill of the abyss creeping!"]},
            {"key": "Infernal Blast", "multiplier": 1.2, "accuracy": 75, "crit": 20, 
             "flavor": ["Burn, burn, burn! Such delightful chaos!", "Feel the heat of my impeccable timing!"]},
            {"key": "Mind Spike", "multiplier": 1.5, "accuracy": 65, "crit": 30, 
             "flavor": ["Your mind trembles, oh how amusing!", "A scream echoes, sweetly orchestrated!"]}
        ]
        self._execute_auto_move(attacks, opponent)

    def _auto_special(self, opponent):
        abilities = [
            {"key": "Soul Drain", "multiplier": 1.8, "accuracy": 85, "crit": 15, "effect": "heal",
             "flavor": ["Ah, the sweet essence of vitality!", "Your soul, a mere sip of delight!"]},
            {"key": "Mana Drain", "multiplier": 1.2, "accuracy": 80, "crit": 10, "effect": "regen",
             "flavor": ["A wave of corrupting energy sweeps the battlefield!", "You feel your power slip away!"]},
            {"key": "Shadow Bind", "multiplier": 0.6, "accuracy": 70, "crit": 5, "effect": "weaken",
             "flavor": ["Struggle all you want, bound you shall be!", "My shadows dance with your futile resistance!"]}
        ]
        self._execute_auto_move(abilities, opponent)

    def _auto_heal(self):
        heal_amount = random.randint(20, 40)
        self.health = min(self.health + heal_amount, self.max_health)
        heal_msg = f"{self.name} casts a dark restorative spell and heals {heal_amount} HP!"
        print(heal_msg)
        self.battle_log.append(heal_msg)
        self.cooldowns["Soul Drain"] = 3  # Add a cooldown for the heal

    def _execute_auto_move(self, moves, opponent):
        # Filter moves that are off cooldown
        available_moves = [m for m in moves if self.cooldowns.get(m["key"], 0) == 0]
        if not available_moves:
            available_moves = moves  # If all on cooldown, just pick one anyway

        chosen = random.choice(available_moves)
        key = chosen["key"]

        # Hit check
        net_hit = max(chosen["accuracy"] - getattr(opponent, "evasion", 0), 5)
        if random.randint(1, 100) > net_hit:
            miss_msg = f"{self.name} casts {key} but misses!"
            print(miss_msg)
            self.battle_log.append(miss_msg)
            self.cooldowns[key] = 1
            return

        # Damage calculation
        base = random.randint(int(self.attack_power * chosen["multiplier"] * 0.8),
                              int(self.attack_power * chosen["multiplier"] * 1.2))
        crit = random.randint(1, 100) <= chosen.get("crit", 0)
        if crit:
            base *= 2
            crit_msg = " 💥 CRITICAL!"
        else:
            crit_msg = ""

        damage = max(int(base) - getattr(opponent, "defense", 0), 0)
        opponent.health = max(opponent.health - damage, 0)

        flavor_msg = random.choice(chosen.get("flavor", ["Magic happens."]))
        print(f"{self.name} uses {key}! {flavor_msg}{crit_msg}")
        print(f"{opponent.name} takes {damage} damage. ({opponent.health} HP left)")

        # Apply effects if special move
        if chosen.get("effect") == "heal":
            heal_amount = damage * 0.5
            self.health = min(self.health + heal_amount, self.max_health)
            print(f"{self.name} siphons life and heals for {heal_amount:.1f} HP!")
        elif chosen.get("effect") == "regen":
            self.regen_active = True
            print(f"{self.name} will regenerate more power next turn!")
        elif chosen.get("effect") == "weaken":
            if hasattr(opponent, "attack_power"):
                old_power = opponent.attack_power
                opponent.attack_power = max(opponent.attack_power * 0.7, 1)
                print(f"{opponent.name}'s attack power reduced from {old_power} to {opponent.attack_power:.1f}!")

        # Update cooldowns
        self.cooldowns[key] = 2
        self.last_move = key
