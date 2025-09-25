from heal import heal
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def battle(player, wizard):
    clear_screen()

    # Intro Dialogue
    print(f"\n Even hell has to do its part to maintain balance in the universe.")
    time.sleep(2)
    print(f"\n If balance is not maintained then we all die.")
    time.sleep(2)
    print(f"\n The earth trembles as {player.name} steps forward...")
    time.sleep(2)
    print("A dark wind howls. Shadows twist. The air thickens with dread.")
    time.sleep(2)
    print(f"{player.name} smirks, eyes locked on the figure ahead.")
    time.sleep(2)
    print(f"\n {wizard.name} emerges from the depths — master of forbidden magic.")
    time.sleep(2)
    print(f"\n Hell hath opened upon this realm, set to disrupt the balance of the universe itself.")
    time.sleep(2)
    print(f"\n Don't forget to smile.")
    time.sleep(2)

    # Optional: Class-specific flavor
    flavor = {
        "ImpAssassin": f"{player.name} I don’t want your gold. I want your gods to flinch.",
        "HellhoundBerserker": f"{player.name} You call it madness. I call it clarity with a side of bloodlust.",
        "DemonSorcerer": f"{player.name} I don’t want control. I want the illusion of control to scream as it dies.",
        "SuccubusRogue": f"{player.name} Chaos is foreplay. Pain is the climax. Shall we begin?"
    }
    print(flavor.get(player.__class__.__name__, f"{player.name} enters the battlefield with silent resolve."))
    time.sleep(2)

    print("\nThe battle begins. Fate hangs in the balance...")
    time.sleep(2)

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
                    result = player.attack(wizard)
                    if result == "end":
                        return
                    elif result is True:
                        player.battle_log.extend(player.battle_log)
                        player.battle_log.clear()
                        player_action_completed = True
                    else:
                        print("Attack failed or blocked. Try a different move.")
                        continue

                elif choice == '2':
                    try:
                        result = player.special_ability(wizard)
                        if result == "end":
                            return
                        elif result is True:
                            player.battle_log.extend(player.battle_log)
                            player.battle_log.clear()
                            player_action_completed = True
                        else:
                            print("Special ability failed or blocked. Try again.")
                            continue
                    except AttributeError:
                        print("Special ability not implemented.")
                        continue

                elif choice == '3':
                    success = heal(player)
                    if success is True:
                        player.battle_log.extend(player.battle_log)
                        player.battle_log.clear()
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

            print("\n Player turn completed. Proceeding to wizard's turn...")

            # ------------------ CHECK WIZARD DEFEAT ------------------
            if wizard.health <= 0:
                print(f"\n🏆 {player.name} has vanquished {wizard.name}! The multiverse lives... for now.")
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

            # Cooldown
            player.reduce_cooldowns()
            wizard.reduce_cooldowns()

            # ------------------ CHECK PLAYER DEFEAT ------------------
            if player.health <= 0:
                print(f"\n💀 {player.name} has fallen. Evil triumphs.")
                print(f"\n The greatest trick that the devil did was convincing the world it doesn't exist")
                time.sleep(2)
                break

            input("\nPress Enter to continue...")
            turn += 1

    except Exception as e:
        print(f"\n An error occurred during battle: {e}")
