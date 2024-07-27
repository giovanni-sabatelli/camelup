from collections import deque
from enum import Enum
import random

class Color(Enum):
    BLUE = 1
    GREEN = 2
    RED = 3
    YELLOW = 4
    PURPLE = 5

class Manager:
    
class Board:
    def __init__(self):
        self.tiles = [Tile() for _ in range(16)]
        for camel in (Camel(color) for color in Color):
            tile_num = random.randint(0, 3)
            self.tiles[tile_num].contents.append(camel)
        self.cards = {color: deque(Card(color, value) for value in (5, 3, 2, 2)) for color in Color}

class Tile:
    def __init__(self):
        self.contents = deque(5)

class Card:    
    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value

class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 3
        self.hand = []

class Camel:
    def __init__(self, color: str):
        self.color = color