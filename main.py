from collections import deque
from enum import Enum
import random
<<<<<<< HEAD
from colorama import Fore, Back, Style
=======
from colorama import init, Back, Style

init(convert=True)

>>>>>>> daae06ddb3f5e603352500f327e1419783db53e8

class Color(Enum):
    BLUE = 0x89CFF0
    GREEN = 0x4F7942
    RED = 0xD2042D
    YELLOW = 0xFFEA00
    MAGENTA = 0x702963


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
        print(self.board)
        player = self.players[self.current_player]
        option = input(f"{player}: Enter 'r' to roll dice or 'b' to place a bet: ")
        if option == "r":
            self.move_camel(player)
            player.money += 1
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
        camel_stack = deque()
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
        self.camel_emojis = {camel: f"{" " * self.camel_pos[camel]}{eval(f"Back.{camel.name}")}🐪{Style.RESET_ALL}" for camel in Color}

    def __str__(self) -> str:
<<<<<<< HEAD
        outstr = ""
        for index in range(4,-1,-1):
            deltaX = 0
            for i in range(len(self.tiles)):
                tile = self.tiles[i]
                if(index >= len(tile.get_camels())):
                    continue
                camel = tile.get_camels()[index]
                outstr += " "+ (" " * (i * 5 - deltaX))  + str(camel) 
                deltaX = 5 + i * 5
            outstr += "\n"
        # tile row
        for i in range(len(self.tiles)):
            if len(str(i+1)) == 1:
                outstr += f"| {i+1}  "
            else:
                #2 digits
                outstr += f"| {i+1} "
        return outstr
=======
        result = ""
        for i in range(4, -1, -1):
            for tile in self.tiles:
                if len(tile.contents) > i:
                    result += f"{self.camel_emojis[tile.contents[i].color]}"
                else:
                    result += " "
            result += "\n"
        return result
                    

>>>>>>> daae06ddb3f5e603352500f327e1419783db53e8

class Camel:
    def __init__(self, color: Color):
        self.color = color
    
    def __str__(self):
        return f"{eval(f"Back.{self.color.name}")} 🐪 {Style.RESET_ALL}"

class Tile:
    def __init__(self):
        self.contents = deque(maxlen=len(Color))

    def add_camel(self, camel: Camel):
        self.contents.append(camel)

    def remove_camel(self) -> Camel:
        return self.contents.pop()

    def get_camels(self):
        return tuple(self.contents)
    
    def __str__(self):
        outstr = ""
        for camel in self.contents:
            outstr += " " +str(camel) + " "
        return outstr
class Card:
    def __init__(self, color: str, value: int):
        self.color = color
        self.value = value


if __name__ == "__main__":
    manager = Manager()
    manager.add_player("Alice")
    manager.add_player("Bob")
    manager.play()
