from heal import heal, reduce_cooldowns

# ====================== BATTLE FUNCTION ============================
def battle(player, wizard):
    try:
        while player.health > 0 and wizard.health > 0:
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
                heal(player) 
            elif choice == '4':
                player.display_stats()
                continue  # Skip wizard's turn
            elif choice == '5':
                print("Quitting game...")
                break
            else:
                print("Invalid choice. Try again.")
                continue

            if wizard.health <= 0:
                print(f"The wizard {wizard.name} has been defeated by {player.name}!")
                break

            print("\n--- Wizard's Turn ---")
            wizard.regenerate()
            wizard.attack(player)

            # Reduce cooldowns after both turns
            reduce_cooldowns(player)

            if player.health <= 0:
                print(f"{player.name} has been defeated!")
                break
    except Exception as e:
        print(f"An error occurred during battle: {e}")
