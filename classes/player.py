"""
docstring
"""

from __future__ import annotations

from exceptions import ActionNotPermitted, ObjectNotFound
from base_classes import GameObject, Item
from equipment import Equipment, Armor, Weapon
from spells import Spell

MAX_HEALTH = 100
MAX_MAGIC = 100

class PlayerCharacter(GameObject):
    health: int = MAX_HEALTH
    magic: int = MAX_MAGIC
    spells: set[Spell] = set()
    gold: int = 0
    inventory: set[Item] = set()
    equipment: set[Equipment] = set()

    @property
    def alive(self) -> bool:
        return self.health > 0
    
    @property
    def armor_rating(self) -> int:
        return sum([a.rating for a in self.armor.values() if a is not None])

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

    def heal(self, hp: int):
        self.health += hp
        if self.health > MAX_HEALTH:
            self.health = MAX_HEALTH
        print(f"Healed up to {self.health}/{MAX_HEALTH} HP.")

    def unequip(self, e: Equipment):
        if e not in self.equipment:
            raise ObjectNotFound(f"Not currently equipped: {e.name}")
        self.equipment.remove(e)
        self.add_to_inventory(e)

    def equip(self, new: Equipment):
        if not isinstance(new, Equipment):
            raise ActionNotPermitted(f"{new.name} cannot be equipped.")
        if new not in self.inventory:
            raise ObjectNotFound(f"Not in inventory: {new.name}")
        for e in self.equipped:
            if isinstance(e, type(new)):
                self.equipment.remove(e)
                self.inventory.add(e)
                break
        self.equipment.add(new)

    def __repr__(self):
        return (
            f"Player(HP: {self.health}, MP: {self.magic}, AR:{self.armor_rating}), "
            f"Inventory: [{len(self.inventory)} items], "
            f"Equipped: [{len(self.equipped)} items], "
            f"Spellbook: [{len(self.spells)} spells]"
        )

