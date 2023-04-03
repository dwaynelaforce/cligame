"""
This module provides the base classes that many other game classes will
inheirit from.
"""

from exceptions import GameObjectNotFound

class GameObject:
    id: str
    name: str
    desc: str

    def __init__(self, conf: dict):
        self.id = conf['id']
        self.name = conf['name']
        self.desc = conf['desc']

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, id={self.id})"

class Item(GameObject):
    @classmethod
    def get_subclass(cls, name: str):
        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass
        raise GameObjectNotFound(name)


class Container(GameObject): 
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