import random

def reduce_cooldowns(character):
    if character.heal_cooldown > 0:
        character.heal_cooldown -= 1


def heal(character):
    heal_cost = getattr(character, 'healing_cost', 50)  # Default to 50 if not set

    if character.gold < heal_cost:
        print(f"{character.name} doesn't have enough gold to heal! ({character.gold} gold available, {heal_cost} required)")
        return

    if character.heal_cooldown > 0:
        print(f"{character.name} can't heal yet! {character.heal_cooldown} turns remaining.")
        return

    heal_amount = random.randint(10, 20)
    character.health = min(character.health + heal_amount, character.max_health)
    character.gold -= heal_cost
    character.heal_cooldown = 3

    print(f"{character.name} heals for {heal_amount} HP at the cost of {heal_cost} gold.")
    print(f"Current health: {character.health}/{character.max_health} | Gold remaining: {character.gold}")
