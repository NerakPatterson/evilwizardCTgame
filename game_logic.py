from classes import *

#---------------Character Creation---------------------
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

#---------------Battle Phase---------------------
def battle(player, wizard):
    try:
        print(f"\nYou face {wizard.name} — HP: {wizard.health}, Attack Power: {wizard.attack_power}")
        turn_count = 1

        while player.health > 0 and wizard.health > 0:
            print(f"\n--- Turn {turn_count} ---")
            print("\n--- Your Turn ---")
            print("1. Attack")
            print("2. Use Special Ability")
            print("3. Heal")
            print("4. View Stats")
            print("5. Quit Game")

            choice = input("\nChoose an action: ")

            if choice == '1':
                player.attack(wizard)
            elif choice == '2':
                try:
                    player.special_ability(wizard)
                except AttributeError:
                    print("Special ability not implemented.")
            elif choice == '3':
                player.heal()  # Or use heal(player) if external
            elif choice == '4':
                player.display_stats()
                wizard.display_stats()
                continue  # Skip wizard's turn
            elif choice == '5':
                print("Quitting game...")
                break
            else:
                print("Invalid choice. Try again.")
                continue

            if wizard.health <= 0:
                print(f"\n🔥 {player.name} has vanquished {wizard.name}! The realm breathes easier... for now.")
                break

            print("\n--- Wizard's Turn ---")
            wizard.regenerate()

            # Check for evade or shield before applying damage
            if getattr(player, 'evade_next', False):
                print(f"{player.name} evades the attack thanks to Vanish!")
                player.evade_next = False
            elif getattr(player, 'shield_active', False):
                print(f"{player.name}'s Divine Shield blocks the attack!")
                player.shield_active = False
            else:
                wizard.attack(player)

            player.reduce_cooldowns()

            if player.health <= 0:
                print(f"\n💀 {player.name} has fallen. Evil triumphs... this time.")
                break

            turn_count += 1

    except Exception as e:
        print(f"An error occurred during battle: {e}")

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
