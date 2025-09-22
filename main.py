from classes import create_character
from classes import EvilWizard
from battle import battle

# ====================== MAIN LOOP ============================
def main():
    while True:
        player = create_character()
        wizard = EvilWizard("The Dark Wizard", health=80, attack_power=15)
        battle(player, wizard)

        restart = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if restart != 'yes':
            print("Thanks for playing!")
            break

# ====================== ENTRY POINT ============================
if __name__ == "__main__":
    main()