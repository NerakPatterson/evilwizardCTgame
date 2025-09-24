import random
from classes import Character
from heal import heal as universal_heal

class DemonSorcerer(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=35)
        self.healing_cost = 50
        self.evade_next = False
        self.last_move = None
        self.current_opponent = None

        # Core stats
        self.accuracy = 85
        self.crit_chance = 20
        self.defense = 4
        self.speed = 35
        self.evasion = 10

        # Cooldowns
        self.cooldowns = {
            "Ignis Anima": 0,
            "Maleficium": 0,
            "Tenebrae Manus": 0,
            "Ars Obscura": 0,
        }

        # Archer-style battle interjections
        self.archer_comments = [
            "Phrasing!",
            "Did anyone bring snacks?",
            "I could do this all day… probably.",
            "I swear, I’m the best at this.",
            "Drink! I mean… spell. Yeah, spell."
        ]

        # Flavor lines per spell
        self.move_insults = {
            "Ignis Anima": [
                "Boom! Soul fire. Bet you didn’t see that coming.",
                "Flames! Hot enough to burn your dignity too."
            ],
            "Maleficium": [
                "Zap! That’s a curse. Hope it stings!",
                "Your face says pain, my heart says 'meh'."
            ],
            "Tenebrae Manus": [
                "Shadow hands grab you… unlucky.",
                "These hands have no chill, unlike me."
            ],
            "Ars Obscura": [
                "Forbidden magic incoming! Don’t blink.",
                "Arcane energy: uncontrolled, unhinged, unstoppable."
            ]
        }

        self.battle_log = []

    def display_stats(self):
        print(f"\n{self.name}'s Stats:")
        print(f" Health: {self.health}/{self.max_health}")
        print(f" Gold: {self.gold}")
        print(f" Defense: {self.defense}")
        print(f" Accuracy: {self.accuracy}")
        print(f" Crit Chance: {self.crit_chance}")
        print(f" Speed: {self.speed}")
        print(f" Evasion: {self.evasion}")

    def heal(self):
        self.heal_amount = 30
        self.heal_cooldown_duration = 2
        print(f"{self.name} mutters: 'Alright, patching myself up…'")
        success = universal_heal(self)
        msg = f"{self.name} {'smirks: There, fixed.' if success else 'groans: That did nothing.'}"
        print(msg)
        self.battle_log.append(msg)
        self._maybe_comment_or_insult()
        return success

    def reduce_cooldowns(self):
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def _maybe_comment_or_insult(self, opponent=None, move_key=None):
        # Random Archer-style interjection
        if random.randint(1, 100) <= 25:
            comment = random.choice(self.archer_comments)
            print(f"{self.name} mutters: '{comment}'")
            self.battle_log.append(comment)
        # Spell-specific flavor
        if opponent and move_key and move_key in self.move_insults and random.randint(1, 100) <= 50:
            insult = random.choice(self.move_insults[move_key])
            print(f"{self.name} sneers at {opponent.name}: '{insult}'")
            self.battle_log.append(insult)

    def _execute_move(self, chosen, opponent):
        key = chosen["key"]
        self.current_opponent = opponent

        # Repeat/cooldown checks
        if self.last_move == key:
            msg = f"{self.name} scoffs: 'Really? {key} again?'"
            print(msg)
            self.battle_log.append(msg)
            return False
        if self.cooldowns.get(key, 0) > 0:
            msg = f"{self.name} deadpans: '{key} cooling down.'"
            print(msg)
            self.battle_log.append(msg)
            return False

        # Accuracy check
        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            msg = f"{self.name} casts {key}… and misses!"
            print(msg)
            self.battle_log.append(msg)
            self._maybe_comment_or_insult(opponent, key)
            self.last_move = key
            self.cooldowns[key] = chosen.get("cooldown", 0)
            return True

        # Damage calculation
        base = self.attack_power * chosen["multiplier"]
        base = random.randint(int(base * 0.8), int(base * 1.2))

        is_crit = random.randint(1, 100) <= chosen.get("crit", 0)
        if is_crit:
            base *= 2
            crit_msg = f"{self.name} grins: 'Critical hit!'"
            print(crit_msg)
            self.battle_log.append(crit_msg)

        damage = max(int(base) - opponent.defense, 0)
        opponent.health = max(opponent.health - damage, 0)

        print(f"\n{self.name} casts {key} — {chosen['description']}")
        flavor_msg = random.choice(self.move_insults.get(key, ["Magic happens."]))
        print(flavor_msg)

        # Random Archer-style interjection
        if random.randint(1, 100) <= 30:
            print(random.choice(self.archer_comments))

        print(f"{opponent.name} takes {damage} damage. Now at {opponent.health} HP.")

        # Optional debuff
        if "debuff" in chosen:
            debuff = chosen["debuff"]
            if not hasattr(opponent, "active_debuffs"):
                opponent.active_debuffs = {}
            opponent.active_debuffs[debuff["stat"]] = {"amount": debuff["amount"], "duration": debuff["duration"]}
            debuff_msg = f"{opponent.name}'s {debuff['stat']} is reduced by {debuff['amount']} for {debuff['duration']} turns!"
            print(debuff_msg)
            self.battle_log.append(debuff_msg)

        self.battle_log.append(f"{self.name} used {key} on {opponent.name} for {damage} damage" + (" (CRIT)" if is_crit else ""))
        self.last_move = key
        self.cooldowns[key] = chosen.get("cooldown", 0)

        # End-of-battle check
        if opponent.health <= 0:
            msg = f"{opponent.name} has been obliterated!"
            print(msg)
            self.battle_log.append(msg)
            return "end"
        if self.health <= 0:
            msg = f"{self.name} has fallen!"
            print(msg)
            self.battle_log.append(msg)
            return "end"

        self._maybe_comment_or_insult(opponent, key)
        return True

    def attack(self, opponent):
        attacks = [
            {"key": "Ignis Anima", "name": "Ignis Anima", "description": "A scorching burst of soul fire.", "multiplier": 1.2, "accuracy": 90, "crit": 25, "cooldown": 1},
            {"key": "Maleficium", "name": "Maleficium", "description": "A dark bolt imbued with a minor curse.", "multiplier": 1.0, "accuracy": 95, "crit": 20, "cooldown": 0, "debuff": {"stat": "attack_power", "amount": 5, "duration": 2}},
        ]
        return self._execute_move(random.choice(attacks), opponent)

    def special_ability(self, opponent):
        abilities = [
            {"key": "Tenebrae Manus", "name": "Tenebrae Manus", "description": "Shadowy hands reduce the foe’s defenses.", "multiplier": 0.8, "accuracy": 85, "crit": 20, "cooldown": 3, "debuff": {"stat": "defense", "amount": 5, "duration": 2}},
            {"key": "Ars Obscura", "name": "Ars Obscura", "description": "A surge of forbidden arcane energy strikes with deadly force.", "multiplier": 1.5, "accuracy": 80, "crit": 30, "cooldown": 4},
        ]
        return self._execute_move(random.choice(abilities), opponent)
