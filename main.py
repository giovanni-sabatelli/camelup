from collections import deque
from enum import Enum
import random
from colorama import init, Back, Style

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
        print(self.board)
        player = self.players[self.current_player]
        option = input(f"{player}: Enter 'r' to roll dice or 'b' to place a bet: ")
        if option == "r":
            self.move_camel(player)
            player.money += 1
        elif option == "b":
            color = input("Enter the color of the camel you want to bet on: ").upper()
            if color in Color.__members__ and self.board.cards[Color[color]][0].value > 0:
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
        tile_pos = self.board.camel_pos[color]
        tile = self.board.tiles[tile_pos]
        camel_stack = []
        while True:
            new_camel = tile.remove_camel()
            camel_stack.append(new_camel)
            if new_camel.color == color:
                break
        end_tile = self.board.tiles[tile_pos+val]
        while len(camel_stack) > 0:
            new_camel = camel_stack.pop()
            end_tile.add_camel(new_camel)
            self.board.camel_pos[new_camel.color] = tile_pos+val

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


class Board:
    def __init__(self):
        self.camel_pos = {color: 0 for color in Color}
        self.tiles = tuple(Tile() for _ in range(16))
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
        out_str = " " * 31
        for color, avail in self.cards.items():
            out_str += f"{avail[0]} "
        out_str += "\n\n"
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
        # Tile Marks row
        for i in range(len(self.tiles)):
            if len(str(i + 1)) == 1:
                out_str += f"| {i + 1}  "
            else:
                out_str += f"| {i + 1} "
        
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
    
    def __str__(self):
        outstr = ""
        for camel in self.contents:
            outstr += " " +str(camel) + " "
        return outstr
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
