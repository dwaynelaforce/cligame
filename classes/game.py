"""
docstring
"""

from __future__ import annotations

import json, sys

from player import PlayerCharacter
from room import Room, ROOMS_DIR, DIRECTIONS
from classes.exceptions import *
from classes.base_classes import Interactable, Item, Container, NPC
from spells import Spell
from combat import CombatEvent

class Game:
    game_over: bool
    player: PlayerCharacter
    room: Room
    visited_rooms: list[Room]
    actions: dict

    def __init__(self):
        self.game_over = False
        self.player = PlayerCharacter()
        self.room = self.load_room("StartingRoom")
        self.visited_rooms = [self.room]
        self.actions = {
            # starts a debug session with variables game, player, room
            'debug': self.debug,
            # goes a direction and loads the next room
            'go': self.go,
            # calls inspect() on the passed local object
            'inspect': self.inspect,
            'inventory': self.player.print_inventory,
            'spells': self.player.print_spellbook,
            'equip': self.player.equip,
            'take': self.room.take_item,
            'open': self.room.open_container,
        }
        self.room.inspect()
        self.game_loop()

    def game_loop(self):
        if not self.player.alive:
            raise GameOver
        cmd = input("\nWhat would you like to do?\n> ").split(" ")
        self.process(cmd)
        self.game_loop()
    
    def process(self, cmd: list[str]):
        try:
            verb, objects = cmd[0], tuple([self.find_object(n) for n in cmd[1:]])
            if verb in ["exit", "quit"]:
                raise GameExit
            if verb not in self.actions:
                raise UnknownAction(verb)
            self.actions[verb](*objects)
        except GameExit as e:
            print(e.__class__.__name__)
            sys.exit()
        except (UnknownAction, ObjectNotFound, RoomNotFound) as e:
            print(e.__class__.__name__, e)

    def go(self, direction: str):
        room_id = getattr(self.room, direction)
        if room_id is None:
            raise RoomNotFound("Can't go that way.")
        if room := self.get_visited_room(room_id):
            self.room = room
        else:
            self.room = self.load_room(room_id)
            self.visited_rooms.append(self.room)
        print(f"You enter {self.room.name}.")
        self.room.inspect()

    def get_visited_room(self, room_id: str) -> Room | None:
        for room in self.visited_rooms:
            if room.id == room_id:
                return room

    def inspect(self, obj: PlayerCharacter|Room|Interactable|Spell):
        obj.inspect()

    def load_room(self, name: str) -> Room:
        path = ROOMS_DIR / f"{name}.json"
        with open(path) as file:
            conf = json.load(file)
        return Room(conf, self.player)

    def find_object(self, name: str) -> str|Room|Interactable|Spell:
        if name in DIRECTIONS:
            return name
        if name == "room":
            return self.room
        if name == "self":
            return self.player
        for interactable in self.room.all_interactables:
            if interactable.name == name:
                return interactable
        for item in self.player.inventory:
            if item.name == name:
                return item
        for spell in self.player.spells:
            if spell.name == name:
                return spell
        raise ObjectNotFound(name)

    def debug(self):
        player = self.player
        room = self.room
        game = self
        breakpoint()