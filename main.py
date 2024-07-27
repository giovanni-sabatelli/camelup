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
    def __init__(self):
        self.board = Board()
        self.players = []
        self.current_player = 0

    def add_player(self, name: str):
        self.players.append(Player(name))

    def play(self):
        while not self.is_game_over():
            self.play_turn()
            self.current_player = (self.current_player + 1) % len(self.players)

    def play_turn(self):
        player = self.players[self.current_player]

    def roll_dice(self) -> tuple[Color, int]:
        color = random.choice(self.board.dice.keys())
        val = self.board.dice[color]
        del self.board.dice[color]
        return (color, val)


class Board:
    def __init__(self):
        self.tiles = tuple(Tile() for _ in range(16))
        for camel in (Camel(color) for color in Color):
            tile_num = random.randint(0, 3)
            self.tiles[tile_num].add_camel(camel)
        self.cards = {
            color: deque(Card(color, value) for value in (5, 3, 2, 2))
            for color in Color
        }
        self.dice = {color: random.randint(1, 3) for color in Color}


class Camel:
    def __init__(self, color: str):
        self.color = color


class Tile:
    def __init__(self):
        self.contents = deque(len(Color))

    def add_camel(self, camel: Camel):
        self.contents.append(camel)

    def remove_camel(self) -> Camel:
        return self.contents.pop()


class Card:
    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value


class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 3
        self.hand = []
