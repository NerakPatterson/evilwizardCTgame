from classes import (
    ImpAssassin,
    HellhoundBerserker,
    DemonSorcerer,
    RedemptionCleric,
    SuccubusRogue,
)

def create_character():
    print("\nChoose your character class:")
    print("1. Imp Assassin  — Agile and evasive")
    print("2. Hellhound Berserker  — Brutal melee damage")
    print("3. Demon Sorcerer  — Unstable magical power")
    print("4. Redemption Cleric  — Healing and shielding")
    print("5. Succubus Rogue  — Charm and gold manipulation")

    choice = input("\nEnter your class number: ")
    name = input("Enter your character's name: ")

    if choice == '1':
        return ImpAssassin(name)
    elif choice == '2':
        return HellhoundBerserker(name)
    elif choice == '3':
        return DemonSorcerer(name)
    elif choice == '4':
        return RedemptionCleric(name)
    elif choice == '5':
        return SuccubusRogue(name)
    else:
        print("Invalid choice. Defaulting to Imp Assassin.")
        return ImpAssassin(name)
