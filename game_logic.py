from classes import *
from imp_assassin import ImpAssassin
from hellhound_berserker import HellhoundBerserker
from demon_sorcerer import DemonSorcerer
from seraphin import Seraphin
from succubus_rogue import SuccubusRogue
from evil_wizard import EvilWizard
import time

#---------------Character Creation---------------------
def create_character():
    print("\nChoose your character class:")
    print("1. Imp Assassin  — Agile and evasive")
    print("2. Hellhound Berserker  — Brutal melee damage")
    print("3. Demon Sorcerer  — Unstable magical power")
    print("4. Seraphin  — Healing and shielding")
    print("5. Succubus Rogue  — Charm and gold manipulation")

    choice = input("\nEnter your class number: ").strip()
    name = input("Enter your character's name: ").strip()

    if choice == '1':
        player = ImpAssassin(name)
        print(f"\n {name}, the shadow-born Imp Assassin, slips from the veil of darkness.")
    elif choice == '2':
        player = HellhoundBerserker(name)
        print(f"\n {name}, the Hellhound Berserker, snarls with fury and bloodlust.")
    elif choice == '3':
        player = DemonSorcerer(name)
        print(f"\n {name}, the Demon Sorcerer, crackles with unstable arcane power.")
    elif choice == '4':
        player = Seraphin(name)
        print(f"\n {name}, the Seraphin, descends with radiant light and divine purpose.")
    elif choice == '5':
        player = SuccubusRogue(name)
        print(f"\n {name}, the Succubus Rogue, smiles with charm and deadly intent.")
    else:
        print("Invalid choice. Defaulting to Imp Assassin.")
        player = ImpAssassin(name)
        print(f"\n {name}, the shadow-born Imp Assassin, slips from the veil of darkness.")

    return player

#---------------Battle Phase---------------------
def battle(player, wizard):
    try:
        print(f"\nThe cursed ruins tremble as {player.name} approaches...")
        time.sleep(2)
        print(f"A dark figure emerges — {wizard.name}, master of forbidden magic.")
        time.sleep(2)
        print(f"\nYou face {wizard.name} — HP: {wizard.health}, Attack Power: {wizard.attack_power}")

        turn = 1
        turn_history = []

        while player.health > 0 and wizard.health > 0:
            print(f"\n=== Turn {turn} ===")
            print("\n--- Your Turn ---")
            player_action_completed = False

            while not player_action_completed:
                print("1. Attack")
                print("2. Use Special Ability")
                print("3. Heal")
                print("4. View Stats")
                print("5. Quit Game")

                choice = input("\nChoose an action: ").strip()

                if choice == '1':
                    player.attack(wizard)
                    turn_history.append(f"{player.name} attacked {wizard.name} for {player.attack_power} damage.")
                    player_action_completed = True

                elif choice == '2':
                    try:
                        player.special_ability(wizard)
                        turn_history.append(f"{player.name} used their special ability.")
                        player_action_completed = True
                    except AttributeError:
                        print("Special ability not implemented.")
                        continue

                elif choice == '3':
                    success = player.heal()
                    if success:
                        turn_history.append(f"{player.name} healed and now has {player.health} HP.")
                        player_action_completed = True
                    else:
                        input("\nHealing failed. Press Enter to choose another action...")
                        continue

                elif choice == '4':
                    player.display_stats()
                    wizard.display_stats()
                    input("\nPress Enter to continue...")
                    continue

                elif choice == '5':
                    print("Quitting game...")
                    return

                else:
                    print("Invalid choice. Try again.")
                    continue

            print("\nPlayer turn completed. Proceeding to wizard's turn...")

            if wizard.health <= 0:
                print(f"\n🏆 {player.name} has vanquished {wizard.name}! The realm breathes easier... for now.")
                turn_history.append(f"{player.name} defeated {wizard.name} in Turn {turn}.")
                break

            print("\n--- Wizard's Turn ---")
            wizard.regenerate()
            time.sleep(1)

            if getattr(player, 'evade_next', False):
                print(f"{player.name} evades the attack thanks to Vanish!")
                turn_history.append(f"{player.name} evaded the attack.")
                player.evade_next = False
            elif getattr(player, 'shield_active', False):
                print(f"{player.name}'s Divine Shield blocks the attack!")
                turn_history.append(f"{player.name}'s shield blocked the attack.")
                player.shield_active = False
            else:
                wizard.attack(player)
                turn_history.append(f"{wizard.name} attacked {player.name} for {wizard.attack_power} damage.")

            player.reduce_cooldowns()

            if player.health <= 0:
                print(f"\n {player.name} has fallen. Evil triumphs... this time.")
                turn_history.append(f"{player.name} was defeated by {wizard.name} in Turn {turn}.")
                break

            turn += 1

        # Show turn history at the end
        print("\n Battle Summary:")
        for entry in turn_history:
            print(f"• {entry}")

    except Exception as e:
        print(f"\n An error occurred during battle: {e}")

#------------------Main---------------
def main():
    while True:
        player = create_character()
        wizard = EvilWizard("The Dark Wizard")
        battle(player, wizard)

        restart = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if restart != 'yes':
            print("Thanks for playing!")
            break

# ====================== ENTRY POINT ============================
if __name__ == "__main__":
    main()
