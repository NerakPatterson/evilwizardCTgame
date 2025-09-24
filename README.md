# Turn-Based Fantasy Combat Game

Welcome to **my turn-based fantasy combat game**!  
Choose a unique character class, face off against the **Evil Wizard**, and unleash strategic abilities in a battle of wits, gold, and survival.

---

## Features

### Playable Classes
Each class has **distinct stats, abilities, and tactical styles**:  

1. **Imp Assassin** – Agile and evasive, uses cunning attacks and critical strikes.  
2. **Hellhound Berserker** – Brutal melee damage with high attack power and ferocious abilities.  
3. **Demon Sorcerer** – Unstable magical power with spell-based attacks and debuffs.  
4. **Succubus Rogue** – Charming attacks, gold manipulation, and evasive maneuvers.

### Enemy AI
- **Evil Wizard**: Main villain NPC with fully automated battle logic.  
  - Randomizes between attacks, special abilities, and healing.  
  - Can regenerate, drain life, and weaken opponents.  
  - Uses cooldowns to prevent spamming and adds unpredictability to battles.  

### Strategic Mechanics
- **Healing**: Costs gold and has cooldowns.  
- **Status Effects**: Evasion, shielding, and buffs/debuffs alter combat dynamics.  
- **Gold Management**: Some abilities steal gold or have risk/reward mechanics.  
- **Variety Between Classes**: Each class has unique move sets and tactical roles.

---

## Modular Architecture

- `classes.py` – Definitions for player classes, enemies, and their abilities.  
- `heal.py` – Universal healing logic and cooldown management.  
- `game_logic.py` – Main game loop and user interface.  
- `battle.py` – Combat flow, battle mechanics, and tactical interactions.  

---

## How to Run

1. Clone or download the project folder.  
2. Ensure all `.py` files are in the same directory.  
3. Run the game from `game_logic.py`:

```bash
python game_logic.py
