import unittest
from main import Manager, Player, Camel, Color

from colorama import Back, Style

class TestCamelUp(unittest.TestCase):
    def setUp(self):
        self.test_manager = Manager()
        self.test_manager.add_player("Alice")
        self.test_manager.add_player("Bob")

    def test_declare_winner_data_type(self):
        self.test_manager.players[0].money = 5
        self.test_manager.players[1].money = 3
        result = self.test_manager.declare_winner()
        self.assertIsInstance(result, str)

    def test_declare_winner(self):
        self.test_manager.players[0].money = 5
        self.test_manager.players[1].money = 3
        expected_result = "Alice wins with 5 coins!"
        result = self.test_manager.declare_winner()
        self.assertEqual(result, expected_result)

    def test_game_over_data_type(self):
        game_over = self.test_manager.is_game_over()
        self.assertIsInstance(game_over, bool)

    def test_game_over1(self):
        game_over = self.test_manager.is_game_over()
        self.assertFalse(game_over)
        
    def test_game_over2(self):
        for i in range(5):
            self.test_manager.roll_dice()
        game_over = self.test_manager.is_game_over()
        self.assertTrue(game_over)

    def test_game_over3(self):
        for i in range(4):
            self.test_manager.roll_dice()
        game_over = self.test_manager.is_game_over()
        self.assertFalse(game_over)
    
    def test_camel1(self):
        camel = Camel(Color.GREEN)
        self.assertEqual(str(camel), f"{Back.GREEN} 🐪 {Style.RESET_ALL}")

    def test_camel2(self):
        camel = Camel(Color.RED)
        self.assertEqual(str(camel), f"{Back.RED} 🐪 {Style.RESET_ALL}")
    
    def test_roll_dice_data_type1(self):
        dice_roll = self.test_manager.roll_dice()
        self.assertIsInstance(dice_roll,tuple)

    def test_roll_dice_data_type_2(self):
        dice_roll = self.test_manager.roll_dice()
        self.assertIsInstance(dice_roll[0],Color)

    def test_roll_dice_data_type_3(self):
        dice_roll = self.test_manager.roll_dice()
        self.assertIsInstance(dice_roll[1],int)

    def test_roll_dice_bounds(self):
        dice_roll = self.test_manager.roll_dice()
        self.assertTrue(dice_roll[1] >= 1)
        
    def test_roll_dice_bounds(self):
        dice_roll = self.test_manager.roll_dice()
        self.assertTrue(dice_roll[1] <= 3)
    


if __name__ == "__main__":
    unittest.main()
