Welcome to my turn-based fantasy combat game! 
Choose a unique character class, face off against the Dark Wizard, and unleash strategic abilities 
in a battle of wits, gold, and survival.

Features:
5 Playable Classes with distinct stats and abilities:
1) Imp Assassin: Agile and evasive
2) Hellhound Berserker: Brutal melee damage
3) Demon Sorcerer: Unstable magical power
4) Redemption Cleric: Healing and shielding
5) Succubus Rogue: Charm and gold manipulation

Enemy AI: The Evil Wizard with regeneration and soul-draining powers
Strategic Mechanics:
Healing with cooldowns and gold cost
Status effects like evasion and shielding
Gold stealing, recoil damage, and regeneration

Modular Architecture:
classes.py: Character definitions and abilities
heal.py: Healing logic and cooldown management
game_logic.py: Main game loop and user interface
battle.py: Combat flow and tactical interactions

How to Run:
Clone or download the project folder
Make sure all .py files are in the same directory
Run the game from game_logic.py:
bash
python game_logic.py

Gameplay Tips:
Healing costs gold and has a cooldown — use it wisely!
Some abilities cause recoil or steal gold — balance risk and reward
Watch for status effects like evade_next and shield_active to avoid damage