"""
docstring
"""

from abc import ABC, abstractmethod

from game_exceptions import *

class Inspectable(ABC):
    """Abstract class for any game asset that can be inspected."""
    @abstractmethod
    def inspect(self): ...

class Interactable(Inspectable):
    id: str
    name: str
    desc: str

    def __init__(self, conf: dict):
        self.id = conf['id']
        self.name = conf['name']
        self.desc = conf['desc']

    def inspect(self):
        print(self.name)
        print(self.desc)

    def __str__(self):
        return self.name

class Item(Interactable):
    @classmethod
    def get_subclass(cls, name: str):
        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass
        raise ObjectNotFound(f"Didn't find Item subclass: {name}")

class Armor(Item):
    body_part: str
    rating: int

    def __init__(self, conf: dict):
        super(Item, self).__init__(conf)
        self.body_part = conf['bodyPart']
        self.rating = conf['rating']

    def inspect(self):
        super().inspect()
        print(f"Armor Rating (AR): {self.rating}")
        print(f"Equips to: {self.body_part}")

    def __str__(self):
        return f"{self.name} | {self.body_part} | AR: {self.rating}"

    def __repr__(self):
        return f"Armor({self.id}, rating: {self.rating}, covers: {self.body_part})"

class Weapon(Item):
    dmg: int

    def __init__(self, conf: dict):
        super(Item, self).__init__(conf)
        self.dmg = conf['dmg']

    def __str__(self):
        return f"{self.name} | dmg: {self.dmg}"

    def __repr__(self):
        return f"Weapon({self.id}, dmg: {self.dmg})"

class SpellTome(Item): ...

class Container(Interactable): 
    locked: bool
    open: bool
    contents: set[Item]

    def __init__(self, conf: dict):
        super().__init__(conf)
        self.closed = conf.get("closed", False)
        self.locked = conf.get("locked", False)
        self.contents = set(
            [Item.get_subclass(i['type'])(i) for i in conf.get("contents", [])]
        )

    def inspect(self):
        super().inspect()
        if self.closed:
            return
        if not self.contents:
            print("It's empty.")
            return
        self.inspect_contents()

    def open_self(self):
        self.closed = False
        self.inspect_contents()

    def inspect_contents(self):
        print(f"In it, you see:")
        for item in self.contents:
            print(f" * {item}")


class NPC(Interactable): 
    health: int