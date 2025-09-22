from heal import heal, reduce_cooldowns
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def battle(player, wizard):
    turn = 1
    try:
        while player.health > 0 and wizard.health > 0:
            clear_screen()
            print(f"\n=== Turn {turn} ===")
            print("=" * 40)

            # ------------------ PLAYER TURN ------------------
            player_action_completed = False

            while not player_action_completed:
                print("\n--- Your Turn ---")
                print("1. Attack")
                print("2. Use Special Ability")
                print("3. Heal")
                print("4. View Stats")
                print("5. Quit Game")

                choice = input("\nChoose an action: ").strip()

                if choice == '1':
                    player.attack(wizard)
                    player_action_completed = True

                elif choice == '2':
                    try:
                        player.special_ability(wizard)
                        player_action_completed = True
                    except AttributeError:
                        print("Special ability not implemented.")
                        continue

                elif choice == '3':
                    success = heal(player)
                    if success:
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

            print("\n✅ Player turn completed. Proceeding to wizard's turn...")

            # ------------------ CHECK WIZARD DEFEAT ------------------
            if wizard.health <= 0:
                print(f"\n🏆 {player.name} has vanquished {wizard.name}! The realm breathes easier... for now.")
                break

            input("\nPress Enter to continue...")

            # ------------------ WIZARD TURN ------------------
            print("\n" + "-" * 40)
            time.sleep(1)
            print("\n--- Wizard's Turn ---")
            wizard.regenerate()
            time.sleep(1)

            if getattr(player, 'evade_next', False):
                print(f"{player.name} evades the attack thanks to Vanish!")
                player.evade_next = False
            elif getattr(player, 'shield_active', False):
                print(f"{player.name}'s Divine Shield blocks the attack!")
                player.shield_active = False
            else:
                wizard.take_turn(player)

            time.sleep(1)
            print("\n--- End of Wizard Turn ---")
            reduce_cooldowns(player)

            # ------------------ CHECK PLAYER DEFEAT ------------------
            if player.health <= 0:
                print(f"\n💀 {player.name} has fallen. Evil triumphs... this time.")
                break

            input("\nPress Enter to continue...")
            turn += 1

    except Exception as e:
        print(f"\n⚠️ An error occurred during battle: {e}")
