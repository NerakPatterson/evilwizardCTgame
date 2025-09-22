import random

def reduce_cooldowns(character):
    if character.heal_cooldown > 0:
        character.heal_cooldown -= 1


def heal(character):
    heal_cost = getattr(character, 'healing_cost', 50)  # Default to 50 if not set
    heal_amount = getattr(character, 'heal_amount', random.randint(10, 20))  # Default healing range

    try:
        #  Full health check
        if character.health == character.max_health:
            raise ValueError(f"{character.name} hasn't taken any damage yet. Healing is not needed.")

        #  Gold check
        if character.gold < heal_cost:
            raise ValueError(f"{character.name} doesn't have enough gold to heal! ({character.gold} available, {heal_cost} required)")

        #  Cooldown check
        if character.heal_cooldown > 0:
            raise ValueError(f"{character.name} can't heal yet! {character.heal_cooldown} turn(s) remaining.")

        #  Healing logic
        character.health = min(character.health + heal_amount, character.max_health)
        character.gold -= heal_cost
        character.heal_cooldown = getattr(character, 'heal_cooldown_duration', 3)

        print(f"\n{character.name} heals for {heal_amount} HP at the cost of {heal_cost} gold.")
        print(f"Current health: {character.health}/{character.max_health} | Gold remaining: {character.gold}")
        return True

    except ValueError as ve:
        print(f"\n Healing failed: {ve}")
        print("Please choose a different action.")
        return False