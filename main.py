from collections import deque
from enum import Enum
import random


class Color(Enum):
    BLUE = 0x89CFF0
    GREEN = 0x4F7942
    RED = 0xD2042D
    YELLOW = 0xFFEA00
    PURPLE = 0x702963


class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 3
        self.hand = []

    def __str__(self) -> str:
        return self.name


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
        print(self.declare_winner())

    def is_game_over(self) -> bool:
        return len(self.board.dice) == 0

    def play_turn(self):
        player = self.players[self.current_player]
        option = input(f"{player}: Enter 'r' to roll dice or 'b' to place a bet: ")
        if option == "r":
            self.move_camel(player)
        elif option == "b":
            color = input("Enter the color of the camel you want to bet on: ").upper()
            if color in Color.__members__:
                color = Color[color]
            else:
                print("Invalid color. Try again.")
                self.play_turn()
            self.place_bet(player, color)
        else:
            print("Invalid input. Try again.")
            self.play_turn()

    def roll_dice(self) -> tuple[Color, int]:
        color = random.choice(tuple(self.board.dice.keys()))
        val = self.board.dice[color]
        del self.board.dice[color]
        return (color, val)

    def move_camel(self, player: Player):
        color, val = self.roll_dice()
        self.board.tiles[val].add_camel(
            self.board.tiles[self.board.camel_pos[color]].remove_camel()
        )
        self.board.camel_pos[color] = val

    def place_bet(self, player: Player, color: Color):
        card = self.board.cards[color].popleft()
        player.hand.append(card)

    def declare_winner(self):
        winner = max(self.players, key=lambda x: x.money)
        return f"{winner} wins with {winner.money} coins!"


class Board:
    def __init__(self):
        self.camel_pos = {color: 0 for color in Color}
        self.tiles = tuple(Tile() for _ in range(16))
        for camel in (Camel(color) for color in Color):
            tile_num = random.randint(0, 2)
            self.tiles[tile_num].add_camel(camel)
            self.camel_pos[camel.color] = tile_num
        self.cards = {
            color: deque(Card(color, value) for value in (5, 3, 2, 2))
            for color in Color
        }
        self.dice = {color: random.randint(1, 3) for color in Color}

    def __str__(self) -> str:
        pass


class Camel:
    def __init__(self, color: str):
        self.color = color


class Tile:
    def __init__(self):
        self.contents = deque(maxlen=len(Color))

    def add_camel(self, camel: Camel):
        self.contents.append(camel)

    def remove_camel(self) -> Camel:
        return self.contents.pop()


class Card:
    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value


if __name__ == "__main__":
    manager = Manager()
    manager.add_player("Alice")
    manager.add_player("Bob")
    manager.play()
