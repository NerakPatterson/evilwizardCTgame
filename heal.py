import random

def reduce_cooldowns(character):
    if hasattr(character, 'heal_cooldown') and character.heal_cooldown > 0:
        character.heal_cooldown -= 1

def heal(character):
    heal_cost = getattr(character, 'healing_cost', 50)
    heal_amount = getattr(character, 'heal_amount', random.randint(10, 20))

    try:
        if character.health == character.max_health:
            raise ValueError(f"{character.name} hasn't taken any damage yet. Healing is not needed.")

        if character.gold < heal_cost:
            raise ValueError(f"{character.name} doesn't have enough gold to heal! ({character.gold} available, {heal_cost} required)")

        if hasattr(character, 'heal_cooldown') and character.heal_cooldown > 0:
            raise ValueError(f"{character.name} can't heal yet! {character.heal_cooldown} turn(s) remaining.")

        character.health = min(character.health + heal_amount, character.max_health)
        character.gold -= heal_cost
        character.heal_cooldown = getattr(character, 'heal_cooldown_duration', 3)

        msg = f"{character.name} heals for {heal_amount} HP at the cost of {heal_cost} gold."
        print(f"\n{msg}")
        print(f"Current health: {character.health}/{character.max_health} | Gold remaining: {character.gold}")
        if hasattr(character, 'battle_log'):
            character.battle_log.append(msg)
        return True

    except ValueError as ve:
        fail_msg = f"Healing failed: {ve}"
        print(f"\n{fail_msg}")
        print("Please choose a different action.")
        if hasattr(character, 'battle_log'):
            character.battle_log.append(fail_msg)
        return False
