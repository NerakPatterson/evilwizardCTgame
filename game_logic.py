from classes import *
from imp_assassin import ImpAssassin
from hellhound_berserker import HellhoundBerserker
from demon_sorcerer import DemonSorcerer
from succubus_rogue import SuccubusRogue
from evil_wizard import EvilWizard
from battle import battle 
import random 

# ====================== CHARACTER CREATION ============================
def create_character():
    print("1. Imp Assassin  — Agile and evasive")
    print("2. Hellhound Berserker  — Brutal melee damage")
    print("3. Demon Sorcerer  — Unstable ASF")
    print("4. Succubus Rogue  — Stealer of Virginity")
    print("5. Random Class  — Let fate decide")

    choice = input("\nEnter your class number: ").strip()
    name = input("Enter your character's name: ").strip()

    if choice == '5':
        choice = random.choice(['1', '2', '3', '4'])
        print(f"\n Fate chooses for you...")

    if choice == '1':
        player = ImpAssassin(name)
        print(f"\n{name}, the shadow-born Imp Assassin, crawling from the charred womb of hell.")
    elif choice == '2':
        player = HellhoundBerserker(name)
        print(f"\n{name}, the Hellhound Berserker, drunk on blood snarls with fury and bloodlust.")
    elif choice == '3':
        player = DemonSorcerer(name)
        print(f"\n{name}, the Demon Sorcerer, cackles with hymns of dissent.")
    elif choice == '4':
        player = SuccubusRogue(name)
        print(f"\n{name}, the Succubus Rogue, smiles with seduction and deadly intent.")
    else:
        print("Invalid choice. Defaulting to Imp Assassin.")
        player = ImpAssassin(name)
        print(f"\n{name}, the shadow-born Imp Assassin, crawling from the charred womb of hell.")

    return player

# ====================== MAIN LOOP ============================
def main():
    while True:
        player = create_character()
        wizard = EvilWizard("The Dark Wizard Billy")
        battle(player, wizard)

        while True:
            restart = input("\nWould you like to play again? (yes/no): ").strip().lower()
            if restart in ['yes', 'y']:
                break  # Restart the game loop
            elif restart in ['no', 'n']:
                print("Thanks for playing!")
                return  #  Exit the game
            else:
                print("Unrecognized input. Please type 'yes', 'y', 'n' or 'no'.")


if __name__ == "__main__":
    main()
