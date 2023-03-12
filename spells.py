"""
docstring
"""

from __future__ import annotations

from interactables import Interactable
# from player import PlayerCharacter
from game_exceptions import GameException

class SpellNotFound(GameException): ...

# abstract base class for spells and meant for retrieving specific spells
class Spell(Interactable):
    magic_cost: int

    def cast(self, target: "PlayerCharacter"|Interactable|None=None): ...
    
    @classmethod
    def get_named_spell(cls, name: str) -> type[Spell]:
        for spelltype in cls.__subclasses__():
            if spelltype.__name__ == name:
                return spelltype
        raise SpellNotFound(name)
    
class HealSelf(Spell):
    magic_cost: int = 5

    @staticmethod
    def cast(self: "PlayerCharacter"):
        self

