import random
from classes import Character
from heal import heal as universal_heal

class HellhoundBerserker(Character):
    def __init__(self, name):
        super().__init__(name, health=180, attack_power=40)
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

        self.comments = [
            "Come with me and I’ll show you the truth, face down in the fountain of youth.",
            "Let’s bury the hatchet… in your head.",
            "Even Van Gogh would call it a bloody good impression!",
            "Wow, truly terrifying... not.",
            "Slave to the plot: let 'em rot or bring 'em back forever.",
            "Try harder next time.",
            "Sometimes… dead is better.",
            "I’m not a hugger. Don’t touch me."
        ]

        self.move_insults = {
            "Snarky Sass": [
                "I’m not a people person. I’m barely a demon person.",
                "I’m not angry. I’m just disappointed… in everything.",
                "I’m not a fan of the ‘fuck you’ attitude, but I’m not above using it."
            ],
            "Moonlight Claws": [
                "You’re like a chihuahua with a gun — loud, twitchy, and way too confident.",
                "Your claws need sharpening… like your skills.",
                "You’re like a hemorrhoid — irritating, painful, and hard to get rid of."
            ],
            "Blood Frenzy": [
                "You’re not worth the therapy I’d need after talking to you.",
                "You’re not intimidating. You’re just tall and annoying.",
                "You’re not edgy. You’re just loud and sad."
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
        print(f"{self.name} growls: 'I’d say ‘bite me,’ but you’d probably cry about it.'")
        success = universal_heal(self)
        msg = f"{self.name} snarls: 'Better. Whatever.'" if success else f"{self.name} snaps: 'Really? Fuck Moxxie!'"
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
            msg = f"{self.name} snarls: 'Come on? {key}, Really?'"
            print(msg)
            self.battle_log.append(msg)
            return False
        if self.cooldowns.get(key, 0) > 0:
            msg = f"{self.name} rolls her eyes: '{key} cooling down Dad. Chill.'"
            print(msg)
            self.battle_log.append(msg)
            return False

        net_hit_chance = max(chosen["accuracy"] - opponent.evasion, 5)
        if random.randint(1, 100) > net_hit_chance:
            msg = f"{self.name} lunges at {opponent.name} but misses. 'I think I drank too much!'"
            print(msg)
            self.battle_log.append(msg)
            self._maybe_comment_or_insult(opponent, key)
            self.last_move = key
            self.cooldowns[key] = chosen.get("cooldown", 0)
            return True

        base = random.randint(
            int(self.attack_power * chosen["multiplier"] * 0.8),
            int(self.attack_power * chosen["multiplier"] * 1.2)
        )
        is_crit = random.randint(1, 100) <= chosen.get("crit", 0)
        if is_crit:
            base *= 2
            crit_msg = f"{self.name} smirks: ' You’re like a bad musical — overacted, underwritten, and nobody asked for it.'"
            print(crit_msg)
            self.battle_log.append(crit_msg)

        damage = max(int(base) - opponent.defense, 0)
        opponent.health = max(opponent.health - damage, 0)
        hit_msg = f"{opponent.name} takes {damage} damage. Now at {opponent.health} HP."
        print(hit_msg)
        self.battle_log.append(f"{self.name} used {key} on {opponent.name} for {damage} damage" + (" (CRIT)" if is_crit else ""))
        self.battle_log.append(hit_msg)

        if "recoil" in chosen:
            recoil_damage = int(self.attack_power * chosen["recoil"])
            self.health = max(self.health - recoil_damage, 0)
            recoil_msg = f"{self.name} winces: 'Worth it... probably.' ({recoil_damage} recoil)"
            print(recoil_msg)
            self.battle_log.append(recoil_msg)

        if "debuff" in chosen:
            debuff = chosen["debuff"]
            if not hasattr(opponent, "active_debuffs"):
                opponent.active_debuffs = {}
            opponent.active_debuffs[debuff["stat"]] = {
                "amount": debuff["amount"],
                "duration": debuff["duration"]
            }
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
            {
                "key": "Snarky Sass",
                "name": "Snarky Sass",
                "description": "A verbal lash that wounds pride.",
                "multiplier": 0.8,
                "accuracy": 95,
                "crit": 5,
                "cooldown": 0,
                "debuff": {"stat": "accuracy", "amount": 10, "duration": 2}
            },
            {
                "key": "Moonlight Claws",
                "name": "Moonlight Claws",
                "description": "A swift slash under moonlight.",
                "multiplier": 1.0,
                "accuracy": 90,
                "crit": 20,
                "cooldown": 0
            }
        ]
        chosen = self.choose_move(attacks)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None  # player chose to go back
    
    def special_ability(self, opponent):
        abilities = [
            {
                "key": "Blood Frenzy",
                "name": "Blood Frenzy",
                "description": "Double damage attack with recoil. May critically strike.",
                "multiplier": 2.0,
                "accuracy": 100,
                "crit": 25,
                "cooldown": 4,
                "recoil": 0.5
            },
            {
                "key": "Infernal Howl",
                "name": "Infernal Howl",
                "description": "A terrifying howl that weakens enemy defense.",
                "multiplier": 1.2,
                "accuracy": 85,
                "crit": 10,
                "cooldown": 3,
                "debuff": {"stat": "defense", "amount": 5, "duration": 3}
            }
        ]
        chosen = self.choose_move(abilities)
        if chosen:
            return self._execute_move(chosen, opponent)
        return None  # player chose to go back
