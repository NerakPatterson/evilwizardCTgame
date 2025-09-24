import random
from classes import Character
from heal import heal as universal_heal

class HellhoundBerserker(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=40)
        self.healing_cost = 65
        self.evade_next = False
        self.last_move = None
        self.battle_log = []
        self.current_opponent = None

        # Core stats
        self.accuracy = 95
        self.crit_chance = 25
        self.defense = 8
        self.speed = 40
        self.evasion = 5

        # Cooldowns
        self.cooldowns = {
            "Blood Frenzy": 0,
            "Infernal Howl": 0,
            "Snarky Sass": 0,
            "Moonlight Claws": 0,
        }

        # Archer-style interjections
        self.archer_comments = [
            "Phrasing!",
            "Do you even lift, mortal?",
            "That was weak. Try again.",
            "Wow, truly terrifying... not.",
            "Classic attempt. Pathetic!",
            "Try harder next time.",
        ]

        # Move-specific insults
        self.move_insults = {
            "Snarky Sass": [
                "Oof, that burn hurt more you than me!",
                "You're really trying… bless your heart.",
                "Keep talking, it’s the only thing you’re good at!"
            ],
            "Moonlight Claws": [
                "Too slow! Are you on vacation or attacking?",
                "Your claws need sharpening… like your skills.",
                "Try harder, I’m barely tickled."
            ],
            "Blood Frenzy": [
                "Look at you, all frothing and… still failing.",
                "I hope that hurt you more than your ego!",
                "Rage all you want, it won’t save you."
            ],
            "Infernal Howl": [
                "That roar was cute. Truly adorable.",
                "Wow, scary… said no one ever.",
                "Is that supposed to intimidate me?"
            ]
        }

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
        self.heal_amount = 20
        self.heal_cooldown_duration = 2
        print(f"{self.name} growls: 'Fine, healing myself... don't get used to it.'")
        success = universal_heal(self)
        msg = f"{self.name} snarls: 'Better. Whatever.'" if success else f"{self.name} snaps: 'Really? Pathetic.'"
        print(msg)
        self.battle_log.append(msg)
        self._maybe_comment_or_insult()
        return success

    def reduce_cooldowns(self):
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def _maybe_comment_or_insult(self, opponent=None, move_key=None):
        # Archer interjection
        if random.randint(1, 100) <= 25:
            comment = random.choice(self.archer_comments)
            print(f"{self.name} mutters: '{comment}'")
            self.battle_log.append(comment)
        # Move-specific insult
        if opponent and move_key and move_key in self.move_insults and random.randint(1, 100) <= 50:
            insult = random.choice(self.move_insults[move_key])
            print(f"{self.name} sneers at {opponent.name}: '{insult}'")
            self.battle_log.append(insult)

    def _execute_move(self, chosen, opponent):
        key = chosen["key"]
        self.current_opponent = opponent

        # Repeat/cooldown checks
        if self.last_move == key:
            msg = f"{self.name} snarls: 'Can't spam {key}, genius!'"
            print(msg)
            self.battle_log.append(msg)
            return False
        if self.cooldowns.get(key, 0) > 0:
            msg = f"{self.name} rolls her eyes: '{key} cooling down. Chill.'"
            print(msg)
            self.battle_log.append(msg)
            return False

        # Accuracy check
        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            msg = f"{self.name} lunges at {opponent.name} but misses. 'Pathetic!'"
            print(msg)
            self.battle_log.append(msg)
            self._maybe_comment_or_insult(opponent, key)
            self.last_move = key
            self.cooldowns[key] = chosen.get("cooldown", 0)
            return True

        # Damage calculation
        base = random.randint(int(self.attack_power * chosen["multiplier"] * 0.8),
                              int(self.attack_power * chosen["multiplier"] * 1.2))
        is_crit = random.randint(1, 100) <= chosen.get("crit", 0)
        if is_crit:
            base *= 2
            crit_msg = f"{self.name} smirks: 'Critical hit! Bet you didn’t see that coming.'"
            print(crit_msg)
            self.battle_log.append(crit_msg)

        damage = max(int(base) - opponent.defense, 0)
        opponent.health = max(opponent.health - damage, 0)
        hit_msg = f"{opponent.name} takes {damage} damage. Now at {opponent.health} HP."
        print(hit_msg)
        self.battle_log.append(f"{self.name} used {key} on {opponent.name} for {damage} damage" + (" (CRIT)" if is_crit else ""))
        self.battle_log.append(hit_msg)

        # Optional debuff
        if "debuff" in chosen:
            debuff = chosen["debuff"]
            if not hasattr(opponent, "active_debuffs"):
                opponent.active_debuffs = {}
            opponent.active_debuffs[debuff["stat"]] = {"amount": debuff["amount"], "duration": debuff["duration"]}
            debuff_msg = f"{opponent.name}'s {debuff['stat']} is reduced by {debuff['amount']} for {debuff['duration']} turns!"
            print(debuff_msg)
            self.battle_log.append(debuff_msg)

        # Archer-style interjection and insult
        self._maybe_comment_or_insult(opponent, key)

        self.last_move = key
        self.cooldowns[key] = chosen.get("cooldown", 0)

        # End of battle check
        if opponent.health <= 0:
            msg = f"{opponent.name} has been defeated!"
            print(msg)
            self.battle_log.append(msg)
            return "end"
        if self.health <= 0:
            msg = f"{self.name} has fallen in battle!"
            print(msg)
            self.battle_log.append(msg)
            return "end"

        return True

    # Normal attacks
    def attack(self, opponent):
        attacks = [
            {"key": "Snarky Sass", "name": "Snarky Sass",
             "description": "A verbal lash that wounds pride.",
             "multiplier": 0.8, "accuracy": 95, "crit": 5, "cooldown": 1,
             "debuff": {"stat": "accuracy", "amount": 10, "duration": 2}},
            {"key": "Moonlight Claws", "name": "Moonlight Claws",
             "description": "A swift slash under moonlight.",
             "multiplier": 1.0, "accuracy": 90, "crit": 20, "cooldown": 0}
        ]
        return self._execute_move(random.choice(attacks), opponent)

    # Special abilities
    def special_ability(self, opponent):
        abilities = [
            {"key": "Blood Frenzy", "name": "Blood Frenzy",
             "description": "Double damage attack with recoil. May critically strike.",
             "multiplier": 2.0, "accuracy": 100, "crit": 25, "cooldown": 3, "recoil": 0.5},
            {"key": "Infernal Howl", "name": "Infernal Howl",
             "description": "A roar that lowers enemy defense temporarily.",
             "multiplier": 1.0, "accuracy": 85, "crit": 10, "cooldown": 4,
             "debuff": {"stat": "defense", "amount": 5, "duration": 2}}
        ]
        return self._execute_move(random.choice(abilities), opponent)
