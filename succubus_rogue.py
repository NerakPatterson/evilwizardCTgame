import random
from classes import Character
from heal import heal as universal_heal

class SuccubusRogue(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power=35)
        self.healing_cost = 50
        self.evade_next = False
        self.last_move = None
        self.battle_log = []
        self.current_opponent = None

        # Core stats
        self.accuracy = 90
        self.crit_chance = 25
        self.defense = 4
        self.speed = 50
        self.evasion = 30

        # Cooldowns
        self.cooldowns = {
            "Seductive Slash": 0,
            "Charm Strike": 0,
            "Tempting Taunt": 0,
            "Lip Lock Laceration": 0,
        }

        self.comments = [
            "You want rules? Cute. I chew rules and spit sarcasm.",
            "I’m not broken. I’m just the part they couldn’t fix without burning the whole thing down.",
            "I used to care. Then I saw what caring gets you — a leash and a therapist.",
            "I don’t want your soul. I want to watch you beg for it back.",
            "I’m not here to kill you. I’m here to make you interesting.",
            "You’re trembling. Is it fear… or anticipation?"
        ]

        self.move_insults = {
            "Seductive Slash": [
                "Ooh, careful! You might cut yourself falling for me.",
                "Too slow, darling. Speed isn’t your forte!",
                "Come on, keep up. You’re embarrassing yourself."
            ],
            "Charm Strike": [
                "Caught ya staring! Distraction is my specialty.",
                "You think you’re immune? Adorable.",
                "That blush suits you… but it won’t save you."
            ],
            "Tempting Taunt": [
                "Every scream is a love letter. Keep writing.",
                "Oh, you’re trying? Cute!",
                "You’re not dying. You’re just becoming art."
            ],
            "Lip Lock Laceration": [
                "They called me a monster. I called them delicious.",
                "Oops… did that sting your ego?",
                "Kisses and cuts, all in a day’s work."
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
        print(f"{self.name} pouts: 'Fine, a little self-care… what's another STD?'")
        success = universal_heal(self)
        msg = f"{self.name} smirks: 'Feeling naughty and nice now.'" if success else f"{self.name} frowns: 'Seriously? I expected better.'"
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
        if random.randint(1, 100) <= 25:
            comment = random.choice(self.comments)
            print(f"{self.name} mutters: '{comment}'")
            self.battle_log.append(comment)
        if opponent and move_key and move_key in self.move_insults and random.randint(1, 100) <= 50:
            insult = random.choice(self.move_insults[move_key])
            print(f"{self.name} sneers at {opponent.name}: '{insult}'")
            self.battle_log.append(insult)

    def _execute_move(self, chosen, opponent):
        key = chosen["key"]
        self.current_opponent = opponent

        print(f"\n{self.name} prepares to use {key}: {chosen['description']}")
        self.battle_log.append(f"{self.name} prepares to use {key}: {chosen['description']}")

        if self.last_move == key:
            msg = f"{self.name} giggles: 'Can't spam {key}, cutie!'"
            print(msg)
            self.battle_log.append(msg)
            return False
        if self.cooldowns.get(key, 0) > 0:
            msg = f"{self.name} rolls her eyes: '{key} cumming soon. Chill out.'"
            print(msg)
            self.battle_log.append(msg)
            return False

        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            msg = f"{self.name} lunges at {opponent.name} but misses. 'Well dammit!'"
            print(msg)
            self.battle_log.append(msg)
            self._maybe_comment_or_insult(opponent, key)
            self.last_move = key
            self.cooldowns[key] = chosen.get("cooldown", 0)
            return True

        base = self.attack_power * chosen["multiplier"]
        base = random.randint(int(base * 0.8), int(base * 1.2))

        is_crit = random.randint(1, 100) <= chosen.get("crit", 0)
        if is_crit:
            base *= 2
            crit_msg = f"{self.name} You think chaos is ugly? Darling, it’s the only thing that ever loved me back.'"
            print(crit_msg)
            self.battle_log.append(crit_msg)

        damage = max(int(base) - opponent.defense, 0)
        opponent.health = max(opponent.health - damage, 0)

        hit_msg = f"{opponent.name} takes {damage} damage. Now at {opponent.health} HP."
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
            {"key": "Seductive Slash", 
             "name": "Seductive Slash", 
             "description": "A flirtatious slash that leaves more than a mark.", 
             "multiplier": 0.9, 
             "accuracy": 95, 
             "crit": 15, 
             "cooldown": 2},
            
            {"key": "Charm Strike", 
             "name": "Charm Strike", 
             "description": 
                 "A dazzling attack that distracts and wounds.", 
             "multiplier": 0.8, 
             "accuracy": 90, 
             "crit": 20, 
             "cooldown": 2}
        ]
        chosen = self.choose_move(attacks)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None

    def special_ability(self, opponent):
        abilities = [
            {
                "key": "Tempting Taunt",
                "name": "Tempting Taunt",
                "description": "A sultry taunt that weakens enemy resolve.",
                "multiplier": 1.0,
                "accuracy": 85,
                "crit": 10,
                "cooldown": 4,
                "debuff": {"stat": "attack_power", "amount": 5, "duration": 2}
            },
            {
                "key": "Lip Lock Laceration",
                "name": "Lip Lock Laceration",
                "description": "A kiss with a deadly twist, can critically strike.",
                "multiplier": 1.5,
                "accuracy": 80,
                "crit": 30,
                "cooldown": 3,
            }
        ]
        chosen = self.choose_move(abilities)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None  
