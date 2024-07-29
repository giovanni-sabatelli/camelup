import unittest
from main import Manager, Player

class TestCamelUp(unittest.TestCase):
	
	def test_declare_winner(self):
		test_manager = Manager()
		test_manager.add_player("Alice")
		test_manager.add_player("Bob")
		test_manager.players[0].money = 5
		test_manager.players[1].money = 3
		expected_result = "Alice wins with 5 coins!"
		result = test_manager.declare_winner()
		self.assertEqual(result, expected_result)

if __name__ == '__main__':
	unittest.main()

