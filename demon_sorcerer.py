import random
from classes import Character
from heal import heal as universal_heal

class DemonSorcerer(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=37)
        self.healing_cost = 50
        self.evade_next = False
        self.last_move = None
        self.current_opponent = None
        self.battle_log = []

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

        self.comments = [
            "I’ve studied the arcane arts, necromancy, and tax evasion.",
            "Welcome to your final exam. Spoiler: you fail, I pass, and your corpse gets extra credit.",
            "I don’t fear death. I RSVP’d centuries ago.",
            "I’m not here to win. I’m here to watch the rules bleed.",
            "The only thing keeping me alive is spite.",
            'I cast spells not to win — but to watch the world forget what mercy felt like.'
        ]

        self.move_insults = {
            "Ignis Anima": [
                "I’m not evil. I’m just extremely disappointed in the universe.",
                "You’re not dying fast enough. Try harder."
                "Every scream is a standing ovation. Keep performing."
            ],
            "Maleficium": [
                "I’ve seen more threatening spells in children’s birthday cards.",
                "Your face says pain, my heart says 'meh'."
                "Chaos doesn’t need a reason. It just needs a stage."
            ],
            "Tenebrae Manus": [
                "Shadow hands grab you…how's that for a hand job?",
                "This is the mostion action you've had in a while isn't it?"
                "I’m not here to win. I’m here to watch the rules bleed."
            ],
            "Ars Obscura": [
                "Your blood screams louder than your battle cries. I like that.",
                "Order is a lie told by cowards. I am the correction."
                "I don’t break minds. I rearrange them until they beg for the voices back."
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
        self.heal_amount = 60
        self.heal_cooldown_duration = 2
        print(f"{self.name} mutters: 'Alright! Don't fucking rush me…'")
        success = universal_heal(self)
        msg = f"{self.name} {'smirks: There, fixed.' if success else 'groans: Well that was lame.'}"
        print(msg)
        self.battle_log.append(msg)
        self._maybe_comment_or_insult()
        return success

    def reduce_cooldowns(self):
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def choose_move(self, move_list):
        print("\nChoose your spell:")
        for i, move in enumerate(move_list, 1):
            key = move["key"]
            cd = self.cooldowns.get(key, 0)
            status = f"(Cooldown: {cd})" if cd > 0 else "(Ready)"
            print(f"{i}. {key} — {move['description']} {status}")
        print(f"{len(move_list)+1}. Go back")

        while True:
            choice = input("Enter spell number: ").strip()
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

        print(f"\n{self.name} prepares to cast {key}: {chosen['description']}")
        self.battle_log.append(f"{self.name} prepares to cast {key}: {chosen['description']}")

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

        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            msg = f"{self.name} casts {key}… and misses!"
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
            crit_msg = f"{self.name} 'Chaos isn’t the absence of control. It’s the moment you realize control was never yours.'"
            print(crit_msg)
            self.battle_log.append(crit_msg)

        damage = max(int(base) - opponent.defense, 0)
        opponent.health = max(opponent.health - damage, 0)

        print(f"{self.name} casts {key} — {chosen['description']}")
        flavor_msg = random.choice(self.move_insults.get(key, ["Magic happens."]))
        print(flavor_msg)

        if random.randint(1, 100) <= 30:
            print(random.choice(self.archer_comments))

        print(f"{opponent.name} takes {damage} damage. Now at {opponent.health} HP.")
        self.battle_log.append(f"{self.name} used {key} on {opponent.name} for {damage} damage" + (" (CRIT)" if is_crit else ""))

        if "debuff" in chosen:
            debuff = chosen["debuff"]
            if not hasattr(opponent, "active_debuffs"):
                opponent.active_debuffs = {}
            opponent.active_debuffs[debuff["stat"]] = {"amount": debuff["amount"], "duration": debuff["duration"]}
            debuff_msg = f"{opponent.name}'s {debuff['stat']} is reduced by {debuff['amount']} for {debuff['duration']} turns!"
            print(debuff_msg)
            self.battle_log.append(debuff_msg)

        self.last_move = key
        self.cooldowns[key] = chosen.get("cooldown", 0)

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
            {"key": "Ignis Anima", 
             "name": "Ignis Anima",
             "description": "A scorching burst of soul fire.",
             "multiplier": 1.2, 
             "accuracy": 90, 
             "crit": 25, 
             "cooldown": 0},
            
            {"key": "Maleficium",
             "name": "Maleficium",
             "description": "A dark bolt imbued with a minor curse.",
             "multiplier": 1.0, 
             "accuracy": 95, 
             "crit": 20, 
             "cooldown": 0,
             "debuff": {"stat": "attack_power", "amount": 5, "duration": 2}}
        ]
        chosen = self.choose_move(attacks)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None

    def special_ability(self, opponent):
        abilities = [
            {"key": "Tenebrae Manus", 
             "name": "Tenebrae Manus",
             "description": "Shadowy hands reduce the foe’s defenses.",
             "multiplier": 0.8, 
             "accuracy": 85, 
             "crit": 20, 
             "cooldown": 4,
             "debuff": {"stat": "defense", "amount": 5, "duration": 2}},
            
            {"key": "Ars Obscura", 
             "name": "Ars Obscura",
             "description": "A surge of forbidden arcane energy strikes with deadly force.",
             "multiplier": 1.5, 
             "accuracy": 80, 
             "crit": 30, 
             "cooldown": 3}
        ]
        chosen = self.choose_move(abilities)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None
