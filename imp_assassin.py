import random
from classes import Character
from heal import heal as universal_heal

class ImpAssassin(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=38)
        self.healing_cost = 55
        self.evade_next = False
        self.last_move = None
        self.battle_log = []
        self.current_opponent = None

        # Core stats
        self.accuracy = 95
        self.crit_chance = 25
        self.defense = 5
        self.speed = 30
        self.evasion = 20

        # Cooldowns
        self.cooldowns = {
            "Shadow Strike": 0,
            "Crotch Kick": 0,
            "Blue Blood Shot": 0,
            "Jugular Slash": 0,
        }

        # Flavor
        self.flavor_comments = [
            "Because I command me too!",
            "Do you even workout?",
            "That was weak. Try again.",
            "Have you tried not sucking?",
            "Blow me bitch!",
            "Wow, that was underwhelming. Try harder!",
            "Classic move… if you’re aiming to suck.",
            "I should’ve known it was you when I could smell fish from a mile away.",
            "If humor is the best medicine, then I’m the devil’s pharmacist!",
        ]

        self.move_insults = {
            "Shadow Strike": [
                "You didn’t even see me coming!",
                "Try aiming next time.",
                "BOO Bitch!"
            ],
            "Crotch Kick": [
                "Ouch… hope that hurt you more than it hurt me to watch!",
                "Low blow! Figuratively and literally.",
                "ROSHAMBO"
            ],
            "Blue Blood Shot": [
                "What's the difference between God and a loaded gun?",
                "Aristocrat Whore!",
                "Royal blood, meet humble pie."
            ],
            "Jugular Slash": [
                "Right for the throat! …Oops, maybe aim better next time.",
                "I'm gonna fuck your neck hole.",
                "Your face!"
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
        self.heal_amount = 50
        self.heal_cooldown_duration = 2
        print(f"{self.name} pulls out a potion with a mischievous grin...")
        success = universal_heal(self)
        msg = f"{self.name} yells: 'Ahhh, that's the stuff! Feeling alive-ish!'" if success else f"{self.name} frowns: 'Ugh, that did nothing! Typical.'"
        print(msg)
        self.battle_log.append(msg)
        self._maybe_comment_or_insult()
        return success

    def reduce_cooldowns(self):
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def choose_move(self, move_list):
        print("\nChoose your move:")
        for i, move in enumerate(move_list, 1):
            key = move["key"]
            cd = self.cooldowns.get(key, 0)
            status = f"(Cooldown: {cd})" if cd > 0 else "(Ready)"
            print(f"{i}. {key} — {move['description']} {status}")
        print(f"{len(move_list)+1}. Go back")

        while True:
            choice = input("Enter move number: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(move_list):
                    return move_list[choice - 1]
                elif choice == len(move_list) + 1:
                    return None
            print("Invalid choice. Try again.")

    def _maybe_comment_or_insult(self, opponent=None, move_key=None):
        if random.randint(1, 100) <= 30:
            comment = random.choice(self.flavor_comments)
            print(f"{self.name} mutters: '{comment}'")
            self.battle_log.append(comment)
        if opponent and move_key and move_key in self.move_insults and random.randint(1, 100) <= 50:
            insult = random.choice(self.move_insults[move_key])
            print(f"{self.name} flips off {opponent.name}: '{insult}'")
            self.battle_log.append(insult)

    def _execute_move(self, chosen, opponent):
        key = chosen["key"]
        self.current_opponent = opponent

        print(f"\n{self.name} prepares to use {key}: {chosen['description']}")
        self.battle_log.append(f"{self.name} prepares to use {key}: {chosen['description']}")

        if self.last_move == key:
            msg = f"{self.name} laughs: 'Can't spam {key}, try harder!'"
            print(msg)
            self.battle_log.append(msg)
            return False
        if self.cooldowns.get(key, 0) > 0:
            msg = f"{self.name} rolls eyes: '{key} cooling down! Patience!'"
            print(msg)
            self.battle_log.append(msg)
            return False

        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            msg = f"{self.name} attacks with {key} but misses! God dammit Moxxie!"
            print(msg)
            self.battle_log.append(msg)
            self._maybe_comment_or_insult(opponent, key)
            self.last_move = key
            self.cooldowns[key] = chosen.get("cooldown", 0)
            return True

        base = random.randint(int(self.attack_power * chosen["multiplier"] * 0.8),
                              int(self.attack_power * chosen["multiplier"] * 1.2))
        is_crit = random.randint(1, 100) <= chosen["crit"]
        if is_crit:
            base *= 2
            crit_msg = f" CRITICAL! {self.name} strikes with {key}!"
            print(crit_msg)
            self.battle_log.append(crit_msg)

        damage = max(int(base) - opponent.defense, 0)
        opponent.health = max(opponent.health - damage, 0)

        hit_msg = f"{opponent.name} takes {damage} damage. Now at {opponent.health} HP."
        print(f"{self.name} uses {key} — {chosen['description']}")
        print(hit_msg)
        self.battle_log.append(f"{self.name} used {key} on {opponent.name} for {damage} damage" + (" (CRIT)" if is_crit else ""))
        self.battle_log.append(hit_msg)

        if "debuff" in chosen:
            debuff = chosen["debuff"]
            if not hasattr(opponent, "active_debuffs"):
                opponent.active_debuffs = {}
            opponent.active_debuffs[debuff["stat"]] = {"amount": debuff["amount"], "duration": debuff["duration"]}
            debuff_msg = f"{opponent.name}'s {debuff['stat']} is reduced by {debuff['amount']} for {debuff['duration']} turns!"
            print(debuff_msg)
            self.battle_log.append(debuff_msg)

        self._maybe_comment_or_insult(opponent, key)

        self.last_move = key
        self.cooldowns[key] = chosen.get("cooldown", 0)

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

    def attack(self, opponent):
        attacks = [
            {"key": "Shadow Strike", 
             "name": "Shadow Strike",
             "description": "A swift stab from the shadows.",
             "multiplier": 1.0, 
             "accuracy": 95, 
             "crit": 20,
             "cooldown": 0},
            
            {"key": "Crotch Kick", 
             "name": "Crotch Kick",
             "description": "A ruthless low blow.",
             "multiplier": 0.7, 
             "accuracy": 90, 
             "crit": 10, 
             "cooldown": 0}
        ]
        chosen = self.choose_move(attacks)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None

    def special_ability(self, opponent):
        abilities = [
            {"key": "Blue Blood Shot",
             "name": "Blue Blood Shot",
             "description": "A special bullet that kills nobles.",
             "multiplier": 1.5, 
             "accuracy": 90, 
             "crit": 25, 
             "cooldown": 3},
            
            {"key": "Jugular Slash", "name": "Jugular Slash",
             "description": "A brutal slash aimed at the throat.",
             "multiplier": 3.0, 
             "accuracy": 70, 
             "crit": 40, 
             "cooldown": 4}
        ]
        chosen = self.choose_move(abilities)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None  # player chose to go back