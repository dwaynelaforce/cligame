"""
docstring
"""

from __future__ import annotations
from typing import Self
from pathlib import Path

from player import PlayerCharacter
from interactables import Interactable, Item, Container, NPC
from game_exceptions import ItemNotFound

ROOMS_DIR = Path("./rooms").absolute()
DIRECTIONS = ["north", "east", "south", "west"]

class Room:
    player: PlayerCharacter
    id: str
    name: str
    text: str
    north: str
    east: str
    south: str
    west: str
    items: set[Item]
    containers: set[Container]
    # npcs: set[NPC]
    actions: dict[str, callable]
    
    def __init__(self, conf: dict, player: PlayerCharacter) -> Self:
        self.player = player
        self.id = conf['id']
        self.name = conf['name']
        self.text = conf['text']
        self.north = conf.get("north", None)
        self.south = conf.get("south", None)
        self.east = conf.get("east", None)
        self.west = conf.get("west", None)
        self.items = {
            Item.get_subclass(i['type'])(i) for i in conf.get("items", [])
        }
        self.containers = {Container(c) for c in conf.get("containers", [])}
        # self.npcs = {NPC(n) for n in conf.get("npcs", [])}

    @property
    def all_interactables(self) -> set[Interactable]:
        interactables = self.items.union(self.containers)
        for container in [c for c in self.containers if not c.closed]:
            interactables = interactables.union(container.contents)
        return interactables

    def inspect(self):
        print(self.name)
        print(self.text)
        inspectables = self.items.union(self.containers)
        if inspectables:
            is_are: str = "is" if len(inspectables) < 2 else "are"
            print(f"In this room there {is_are}:")
            for i in inspectables:
                print(f" * {i}")
        else:
            print("It doesn't look like there is anything of note here.")
        self.print_available_dirs()

    def print_available_dirs(self):
        print("From here you can go:")
        if self.north:
            print(" * north")
        if self.east:
            print(" * east")
        if self.south:
            print(" * south")
        if self.west:
            print(" * west")

    def print_interactables(self):
        if not self.all_interactables:
            return
        is_are = "is" if len(self.all_interactables) < 2 else "are"
        print(f"In this room there {is_are}:")
        for i in self.all_interactables:
            print(f" * {i.name}")

    def take_item(self, item: Item):
        if item in self.items:
            self.items.remove(item)
            self.player.add_to_inventory(item)
            return
        for container in [c for c in self.containers if not c.closed]:
            if item in container.contents:
                container.contents.remove(item)
                self.player.add_to_inventory(item)
                return
        raise ItemNotFound

    def open_container(self, container: Container):
        if container.locked:
            print("It's locked.")
            return
        print(f"You open the {container.name}.")
        container.closed = False
        if container.contents:
            print("Inside you see:")
            for item in container.contents:
                print(f" * {item}")
        else:
            print("It's empty.")

    def __repr__(self):
        return f"Room({self.id}, [{self.all_interactables} interactables])"