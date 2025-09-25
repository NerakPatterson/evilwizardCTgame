class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.gold = 250
        self.heal_uses_remaining = 5
        self.heal_cooldown = 0
        self.last_move = None
        self.cooldowns = {}
        self.battle_log = []

    def reduce_cooldowns(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        for move in self.cooldowns:
            if self.cooldowns[move] > 0:
                self.cooldowns[move] -= 1

    def is_alive(self):
        return self.health > 0

    def reset(self):
        self.health = self.max_health
        self.gold = 250
        self.heal_uses_remaining = 5
        self.heal_cooldown = 0
        self.cooldowns = {move: 0 for move in self.cooldowns}
        self.battle_log.clear()

    def display_stats(self):
        print("\n Character Stats:")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Gold: {self.gold}")
        print(f"Heals Remaining: {self.heal_uses_remaining}")
        print(f"Heal Cooldown: {self.heal_cooldown}")
        print("Cooldowns:")
        for move, cd in self.cooldowns.items():
            status = "Ready" if cd == 0 else f"{cd} turn(s)"
            print(f"  {move}: {status}")

    def view_stats(self, opponent):
        self.display_stats()
        print("\n🧟 Enemy Stats:")
        print(f"Name: {opponent.name}")
        print(f"Health: {opponent.health}/{opponent.max_health}")
        print(f"Attack Power: {opponent.attack_power}")

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
                    break

                elif choice == "2":
                    self.special_ability(opponent)
                    break

                elif choice == "3":
                    success = self.heal()
                    if success:
                        break
                    else:
                        continue

                elif choice == "4":
                    print(f"{self.name} hesitates and skips their turn.")
                    break

                elif choice == "5":
                    self.view_stats(opponent)
                    continue

                else:
                    raise ValueError("Invalid menu option. Please enter a number from 1 to 5.")

            except AttributeError as e:
                print(f"\nAction failed: {e}")
                print("This character may not have that ability. Try a different option.")
                continue

            except ValueError as ve:
                print(f"\n{ve}")
                continue

            except Exception as e:
                print(f"\nUnexpected error: {e}")
                continue
