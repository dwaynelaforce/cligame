from base_classes import Item

class Equipment(Item): ...

class Armor(Equipment):
    rating: int

    def inspect(self):
        super().inspect()
        print(f"Armor Rating (AR): {self.rating}")
        print(f"Equips to: {self.body_part}")

    def __str__(self):
        return f"{self.name} | AR: {self.rating}"

class Helmet(Armor): ...

class Armwear(Armor): ...

class Footwear(Armor): ...

class ChestArmor(Armor): ...

class Weapon(Equipment):
    dmg: int

    def __str__(self):
        return f"{self.name} | DMG: {self.dmg}"

    def __repr__(self):
        return f"Weapon({self.name}, id={self.id}, dmg: {self.dmg})"
