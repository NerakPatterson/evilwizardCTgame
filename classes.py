# ====================== CHARACTER CREATION ============================
def create_character():
    name = input("Enter your character's name: ")
    return Character(name, health=100, attack_power=20)

# ====================== BASE CHARACTER CLASS ============================
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health
        self.gold = 1000
        self.heal_cooldown = 0
        self.last_move = None
        self.cooldowns = {}  # Each subclass will define its own moves here

    def reduce_cooldowns(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def choose_action(self, opponent):
        while True:
            print("\nChoose your action:")
            print("1. Attack")
            print("2. Special Ability")
            print("3. Heal")
            print("4. Cancel Turn")
            print("5. View Stats")

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self.attack(opponent)
                    break  # valid action, end turn

                elif choice == "2":
                    self.special_ability(opponent)
                    break  # valid action, end turn

                elif choice == "3":
                    success = self.heal()
                    if success:
                        break  # healing succeeded
                    else:
                        continue  # healing failed, retry turn

                elif choice == "4":
                    print(f"{self.name} hesitates and skips their turn.")
                    break  # intentional skip

                elif choice == "5":
                    self.view_stats(opponent)
                    continue  # loop continues after viewing stats

                else:
                    raise ValueError("Invalid menu option. Please enter a number from 1 to 5.")

            except AttributeError as e:
                print(f"\nAction failed: {e}")
                print("This character may not have that ability. Try a different option.")
                continue  # retry turn

            except ValueError as ve:
                print(f"\n{ve}")
                continue  # retry turn

            except Exception as e:
                print(f"\nUnexpected error: {e}")
                print("Something went wrong. Please try a different action.")
                continue  # retry turn

    def view_stats(self, opponent):
        while True:
            print("\nCharacter Stats:")
            print(f"Name: {self.name}")
            print(f"Health: {self.health}/{self.max_health}")
            print(f"Attack Power: {self.attack_power}")
            print(f"Gold: {self.gold}")
            print(f"Heal Cooldown: {self.heal_cooldown}")
            print("Cooldowns:")
            for move, cd in self.cooldowns.items():
                status = "Ready" if cd == 0 else f"{cd} turn(s)"
                print(f"  {move}: {status}")

            print("\n🧟 Enemy Stats:")
            print(f"Name: {opponent.name}")
            print(f"Health: {opponent.health}/{opponent.max_health}")
            print(f"Attack Power: {opponent.attack_power}")

            print("\nPress B to go back.")
            back = input(">> ").strip().upper()
            if back == "B":
                return
            else:
                print("Invalid input. Press B to return.")