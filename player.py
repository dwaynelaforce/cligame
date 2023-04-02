"""
docstring
"""

from __future__ import annotations

from typing import Union

from game_exceptions import ItemNotFound
from interactables import Inspectable, Item, Armor, Weapon
from spells import Spell

MAX_HEALTH = 100
MAX_MAGIC = 100

class PlayerCharacter(Inspectable):
    health: int = MAX_HEALTH
    magic: int = MAX_MAGIC
    spells: set[Spell] = set()
    gold: int = 0
    inventory: set[Item] = set()
    armor: dict[str, Armor|None] = {
        'head': None,
        'torso': None,
        'arms': None,
        'legs': None,
    }
    weapon: Weapon|None = None

    @property
    def alive(self) -> bool:
        return self.health > 0
    
    @property
    def armor_rating(self) -> int:
        return sum([a.rating for a in self.armor.values() if a is not None])
    
    @property
    def equipped(self) -> set[Item]:
        return {
            e for e in (list(self.armor.values()) + [self.weapon]) if e is not None
        }

    def print_inventory(self):
        print(f"Inventory: [{self.gold} gold, {len(self.inventory)} items]")
        for item in self.inventory:
            print(f" * {item}")

    def print_spellbook(self):
        print(f"Spellbook: [{len(self.spells)} spells]")
        for spell in self.spells:
            print(spell)

    def print_equipped(self):
        print(f"Equipped: [{len(self.equipped)} items]")
        for item in self.equipped:
            print(f" * {item}")

    def inspect(self):
        print("Player Info:")
        print(f"Health: {self.health}/{MAX_HEALTH}")
        print(f"Magic: {self.magic}/{MAX_MAGIC}")
        print(f"Armor Rating: {self.armor_rating}")
        self.print_equipped()
        self.print_inventory()
        self.print_spellbook()

    def add_to_inventory(self, item: Item):
        self.inventory.add(item)
        print(f"You take the {item.name} into your inventory.")

    def heal(self, amt: int):
        self.health += amt
        if self.health > MAX_HEALTH:
            self.health = MAX_HEALTH
        print(f"Healed up to {self.health}/{MAX_HEALTH} HP.")

    def equip(self, item: Armor|Weapon):
        if item not in self.inventory:
            raise ItemNotFound(f"Didn't find {item.name} in inventory.")
        if isinstance(item, Armor):
            self.armor[item.body_part] = item
        elif isinstance(item, Weapon):
            self.weapon = item
        self.inventory.remove(item)

    def __repr__(self):
        return (
            f"Player(HP: {self.health}, MP: {self.magic}, AR:{self.armor_rating}), "
            f"Inventory: [{len(self.inventory)} items], "
            f"Equipped: [{len(self.equipped)} items], "
            f"Spellbook: [{len(self.spells)} spells]"
        )

