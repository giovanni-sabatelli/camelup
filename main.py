from collections import deque, defaultdict
from enum import Enum
import random
from colorama import init, Back, Style
from copy import deepcopy
from itertools import product, permutations
from math import factorial

init(convert=True)

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
        self.last_message = "Welcome to Camel Up!\n"
        self.players = []
        self.current_player = 0

    def add_player(self, name: str):
        self.players.append(Player(name))

    def play(self):
        while not self.is_game_over():
            self.play_turn()
            self.current_player = (self.current_player + 1) % len(self.players)
        self.cash_bets()
        print(self.declare_winner())

    def is_game_over(self) -> bool:
        return len(self.board.dice) == 0

    def play_turn(self):
        print(f"\n{self.board}\n")
        print(self.last_message, end="")
        print(", ".join(f"{c.name.title()}: {round(v, 5)}" for c, v in self.calc_ev(not("rolled" in self.last_message or "elcome" in self.last_message)).items()) + "\n")
        player = self.players[self.current_player]
        option = input(f"{player}: Enter 'r' to roll dice or 'b' to place a bet: ")
        if option == "r":
            roll_message = self.move_camel(player, *self.roll_dice())
            player.money += 1
            self.last_message = f"{self.players[self.current_player]} rolled {roll_message}\n"
        elif option == "b":
            color = input("Enter the color of the camel you want to bet on: ").upper()
            if color in Color.__members__ and self.board.cards[Color[color]][0].value > 0:
                color = Color[color]
                self.last_message = f"{self.players[self.current_player]} picked up the {color.name.title()} wager\n"
                self.place_bet(player, color)
            else:
                print("Invalid color. Try again.")
                self.play_turn()
        else:
            print("Invalid input. Try again.")
            self.play_turn()

    def roll_dice(self) -> tuple[Color, int]:
        color = random.choice(tuple(self.board.dice.keys()))
        val = self.board.dice[color]
        del self.board.dice[color]
        return (color, val)

    def move_camel(self, player: Player, color: Color, val: int) -> str:
        tile_pos = self.board.camel_pos[color]
        tile = self.board.tiles[tile_pos]
        camel_stack = deque()
        while True:
            new_camel = tile.remove_camel()
            camel_stack.append(new_camel)
            if new_camel.color == color:
                break
        end_tile = self.board.tiles[tile_pos + val]
        while len(camel_stack) > 0:
            new_camel = camel_stack.pop()
            end_tile.add_camel(new_camel)
            self.board.camel_pos[new_camel.color] = tile_pos + val
        return f"{color.name.title()} - {val}"

    def place_bet(self, player: Player, color: Color):
        if self.board.cards[color][0] == 0:
            print("No more bets available for this camel.")
            return
        card = self.board.cards[color].popleft()
        player.hand.append(card)

    def declare_winner(self):
        winner = max(self.players, key=lambda x: x.money)
        return f"{winner} wins with {winner.money} coins!"
    
    def cash_bets(self):
        order = []
        for tile in self.board.tiles:
            for camel in tile.get_camels():
                order.append(camel)
        for player in self.players:
            for card in player.hand:
                if card.color == order[len(order) - 1].color:
                    player.money += card.value
                elif card.color == order[len(order) - 2].color:
                    player.money += 1
                else:
                    player.money -= 1
    
    def calc_ev(self,done:bool) -> dict[Color, float]:
        length = len(self.board.dice)
        if not done:
            places = defaultdict(lambda: [0, 0, 0, 0, 0])
            for roll in product(range(1, 4), repeat=length):
                for order in permutations(tuple((k, roll[i]) for i, k in enumerate(self.board.dice)), length):
                    temp = deepcopy(self)
                    for move in order:
                        temp.move_camel(temp.current_player, *move)
                    j = 0
                    for tile in temp.board.tiles:
                        if j == 5:
                            break
                        for camel in tile.get_camels():
                            places[camel.color][j] += 1
                            j += 1
            self.places = places
        return {c: (n[4] * self.board.cards[c][0].value + n[3] - n[2] - n[1] - n[0]) / (factorial(length) * 3 ** length) for c, n in self.places.items() if self.board.cards[c][0].value != 0}



class Board:
    def __init__(self):
        self.camel_pos = {color: 0 for color in Color}
        self.tiles = tuple(Tile() for _ in range(18))
        for camel in (Camel(color) for color in Color):
            tile_num = random.randint(0, 2)
            self.tiles[tile_num].add_camel(camel)
            self.camel_pos[camel.color] = tile_num
        self.cards = {
            color: deque(Card(color, value) for value in (5, 3, 2, 2, 0))
            for color in Color
        }
        self.dice = {color: random.randint(1, 3) for color in Color}
        self.camel_emojis = {camel: f"{" " * self.camel_pos[camel]}{eval(f"Back.{camel.name}")}🐪{Style.RESET_ALL}" for camel in Color}

    def __str__(self) -> str:
        out_str = " " * 31 + "".join(f"{avail[0]} " if avail[0].value > 0 else " " * 4 for avail in self.cards.values()) + "\n\n"
        for ind in range(4, -1, -1):
            dx = 0
            for i in range(len(self.tiles)):
                tile = self.tiles[i]
                if ind >= len(tile.get_camels()):
                    continue
                camel = tile.get_camels()[ind]
                out_str += " " + (" " * (i * 5 - dx)) + str(camel) 
                dx = 5 + i * 5
            if dx > 0:
                out_str += "\n"
        for i in range(len(self.tiles)):
            out_str += f"| {i + 1}" + " " * (3 - len(str(i + 1)))
        
        return out_str
                    
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
    
class Card:
    def __init__(self, color: Color, value: int):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{eval(f"Back.{self.color.name}")} {self.value} {Style.RESET_ALL}"

if __name__ == "__main__":
    manager = Manager()
    manager.add_player("Alice")
    manager.add_player("Bob")
    manager.play()
