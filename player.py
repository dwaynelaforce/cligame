"""
docstring
"""

from __future__ import annotations

from typing import Union

from game_exceptions import ItemNotFound
from interactables import Item, Armor, Weapon
from spells import Spell

MAX_HEALTH = 100
MAX_MAGIC = 100

class PlayerCharacter:
    health: int = MAX_HEALTH
    magic: int = MAX_MAGIC
    spells: set[Spell] = set()
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
    
    def print_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
            return
        print("Inventory:")
        for item in self.inventory:
            print(f" * {item}")

    def print_spellbook(self):
        if not self.spells:
            print("No spells in spellbook.")
            return
        print("Spells:")
        for spell in self.spells:
            print(spell)

    def inspect(self):
        print("Player Info:")
        print(f"Health {self.health}/{MAX_HEALTH}")
        print(f"Magic {self.magic}/{MAX_MAGIC}")
        print(f"Armor Rating {self.armor_rating}")
        equipped = [self.weapon] + [a for a in self.armor.values()]
        equipped = [e for e in equipped if e is not None]
        print(f"Equipped: {len(equipped)} items")
        for item in equipped:
            print(f" * {item}")

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
        equipped_ct = ... # TODO count equipped items correctly
        return (
            f"Player(HP: {self.health}, MP: {self.magic}, AR:{self.armor_rating}), "
            f"Inventory: [{len(self.inventory)} items], Equipped: [{equipped_ct} items]]"
        )

