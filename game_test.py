import unittest
from game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.board = [
            ['a', 'b', 'b'],
            ['b', 'a', 'b'],
            ['b', 'c', 'b']]
        self.game.score = 0
        self.game.winner = False
        self.game.board_size = 3
        self.game.target_score_to_win = 100

    def test_set_up_board(self):
        self.game.board = [[None for _ in range(self.game.board_size)] for _ in range(self.game.board_size)]
        self.game.set_up_board()
        for row in range(self.game.board_size):
            for column in range(self.game.board_size):
                self.assertTrue(self.game.board[row][column])

    def test_get_neighbor_items(self):
        '''[left, right, lower, upper]'''
        self.assertEqual(Game.get_neighbor_items(self.game, 1, 0), [None, 'a', 'b', 'a'])
        self.assertEqual(Game.get_neighbor_items(self.game, 2, 2), ['c', None, None, 'b'])
        self.assertEqual(Game.get_neighbor_items(self.game, 0, 0), [None, 'b', 'b', None])
        self.assertEqual(Game.get_neighbor_items(self.game, 1, 1), ['b', 'b', 'c', 'b'])
        self.assertEqual(Game.get_neighbor_items(self.game, 1, 2), ['a', None, 'b', 'b'])

    def test_get_neighbor_coordinates(self):
        '''[left, right, lower, upper]'''
        self.assertEqual(Game.get_neighbor_coordinates(self.game, 1, 0), [None, (1, 1), (2, 0), (0, 0)])
        self.assertEqual(Game.get_neighbor_coordinates(self.game, 2, 2), [(2, 1), None, None, (1, 2)])
        self.assertEqual(Game.get_neighbor_coordinates(self.game, 0, 0), [None, (0, 1), (1, 0), None])
        self.assertEqual(Game.get_neighbor_coordinates(self.game, 1, 1), [(1, 0), (1, 2), (2, 1), (0, 1)])
        self.assertEqual(Game.get_neighbor_coordinates(self.game, 1, 2), [(1, 1), None, (2, 2), (0, 2)])

    def test_there_is_row_above(self):
        for row, boolean in enumerate([False, True, True]):
            self.assertEqual(self.game.there_is_row_above(row), boolean)

    def test_1_delete_items(self):
        indices_items_to_delete = {(2, 0), (1, 0)}
        Game.delete_items(self.game, indices_items_to_delete)
        new_board = [
            ['a', 'b', 'b'],
            [None, 'a', 'b'],
            [None, 'c', 'b']]
        self.assertEqual(self.game.board, new_board)

    def test_2_delete_items(self):
        indices_items_to_delete = {(2, 2), (2, 1)}
        Game.delete_items(self.game, indices_items_to_delete)
        new_board = [
            ['a', 'b', 'b'],
            ['b', 'a', 'b'],
            ['b', None, None]]
        self.assertEqual(self.game.board, new_board)

    def test_next_move_is_available(self):
        self.game.board = [
            ['a', 'c', 'a'],
            ['b', 'a', 'b'],
            ['b', 'c', 'b']]
        self.assertFalse(self.game.next_move_is_available())
        self.game.board = [
            ['a', 'b', 'c'],
            ['b', 'a', 'b'],
            ['b', 'b', 'a']]
        self.assertTrue(self.game.next_move_is_available())

    def test_1_swap_items(self):
        lower_item = 2, 1
        upper_item = 1, 1
        self.game.board = [
            ['a', 'b', 'b'],
            ['b', 'a', 'b'],
            ['b', None, 'b']]
        self.game.swap_items(*lower_item, *upper_item)
        new_board = [
            ['a', 'b', 'b'],
            ['b', None, 'b'],
            ['b', 'a', 'b']]
        self.assertEqual(self.game.board, new_board)

    def test_2_swap_items(self):
        lower_item = 2, 0
        upper_item = 0, 0
        self.game.board = [
            ['a', 'b', 'b'],
            ['b', 'a', 'b'],
            [None, 'c', 'b']]
        self.game.swap_items(*lower_item, *upper_item)
        new_board = [
            [None, 'b', 'b'],
            ['b', 'a', 'b'],
            ['a', 'c', 'b']]
        self.assertEqual(self.game.board, new_board)

    def test_3_swap_items(self):
        lower_item = 1, 2
        upper_item = 0, 2
        self.game.board = [
            ['a', 'b', 'b'],
            ['b', 'a', None],
            ['b', 'c', 'b']]
        self.game.swap_items(*lower_item, *upper_item)
        new_board = [
            ['a', 'b', None],
            ['b', 'a', 'b'],
            ['b', 'c', 'b']]
        self.assertEqual(self.game.board, new_board)

    def test_1_replace_single_item(self):
        self.game.board = [
            ['a', 'b', 'b'],
            ['b', None, 'b'],
            ['b', None, 'b']]
        self.game.replace_single_item(2, 1)
        new_board = [
            ['a', None, 'b'],
            ['b', None, 'b'],
            ['b', 'b', 'b']]
        self.assertEqual(self.game.board, new_board)

    def test_2_replace_single_item(self):
        self.game.board = [
            ['a', 'b', 'b'],
            ['b', 'c', 'c'],
            ['b', 'a', None]]
        self.game.replace_single_item(2, 2)
        new_board = [
            ['a', 'b', 'b'],
            ['b', 'c', None],
            ['b', 'a', 'c']]
        self.assertEqual(self.game.board, new_board)

    def test_1_replace_items(self):
        indices_items_to_replace = [(0, 0), (1, 0)]
        self.game.board = [
            [None, 'b', 'b'],
            [None, 'a', 'b'],
            ['a', 'c', 'b']]
        self.game.replace_items(indices_items_to_replace)
        self.assertFalse(self.game.board[0][0], None)
        self.assertFalse(self.game.board[1][0], None)

    def test_2_replace_items(self):
        indices_items_to_replace = [(2, 1), (1, 1)]
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', None, 'b'],
            ['a', None, 'b']]
        indices_create_new_items = self.game.replace_items(indices_items_to_replace)
        new_board = [
            ['c', None, 'b'],
            ['b', None, 'b'],
            ['a', 'b', 'b']]
        self.assertTrue(indices_create_new_items == [(1, 1), (0, 1)])
        self.assertEqual(self.game.board, new_board)

    def test_create_random_item(self):
        self.game.board = [
            ['a', None, 'b'],
            ['b', None, 'b'],
            ['b', 'a', 'c']]
        indices_create_new_items = [(0, 1), (1, 1)]
        self.game.create_new_items(indices_create_new_items)
        self.assertTrue(self.game.board[0][1])
        self.assertTrue(self.game.board[1][1])

    '''TEST COMPLETE GAME CYCLE - 1'''

    def test_1_get_indices_items_to_delete(self):
        self.game.board = [
            ['c', 'a', 'c'],
            ['b', 'b', 'b'],
            ['b', 'c', 'a']]
        correct_indices_items_to_delete = {(2, 0), (1, 0), (1, 1), (1, 2)}
        indices_items_to_delete = self.game.get_indices_items_to_delete(2, 0)
        self.assertEqual(indices_items_to_delete, correct_indices_items_to_delete)

    def test_3_delete_items(self):
        indices_items_to_delete = {(2, 0), (1, 0), (1, 1), (1, 2)}
        self.game.board = [
            ['c', 'a', 'c'],
            ['b', 'b', 'b'],
            ['b', 'c', 'a']]
        Game.delete_items(self.game, indices_items_to_delete)
        new_board = [
            ['c', 'a', 'c'],
            [None, None, None],
            [None, 'c', 'a']]
        self.assertEqual(self.game.board, new_board)

    def test_3_replace_items(self):
        indices_items_to_replace = [(2, 0), (1, 2), (1, 1), (1, 0)]
        self.game.board = [
            ['c', 'a', 'c'],
            [None, None, None],
            [None, 'c', 'a']]
        self.game.replace_items(indices_items_to_replace)
        new_board = [
            [None, None, None],
            [None, 'a', 'c'],
            ['c', 'c', 'a']]
        self.assertEqual(self.game.board, new_board)

    def test_3_replace_single_item(self):
        self.game.board = [
            ['c', 'a', 'c'],
            [None, None, None],
            [None, 'c', 'a']]
        self.game.replace_single_item(2, 0)
        new_board = [
            [None, 'a', 'c'],
            [None, None, None],
            ['c', 'c', 'a']]
        self.assertEqual(self.game.board, new_board)

    def test_4_replace_single_item(self):
        self.game.board = [
            ['c', 'a', 'c'],
            [None, None, None],
            [None, 'c', 'a']]
        self.game.replace_single_item(1, 2)
        new_board = [
            ['c', 'a', None],
            [None, None, 'c'],
            [None, 'c', 'a']]
        self.assertEqual(self.game.board, new_board)

    def test_5_replace_single_item(self):
        self.game.board = [
            ['c', 'a', 'c'],
            [None, None, None],
            [None, 'c', 'a']]
        self.game.replace_single_item(1, 1)
        new_board = [
            ['c', None, 'c'],
            [None, 'a', None],
            [None, 'c', 'a']]
        self.assertEqual(self.game.board, new_board)

    def test_6_replace_single_item(self):
        self.game.board = [
            ['c', 'a', 'c'],
            [None, None, None],
            [None, 'c', 'a']]
        self.game.replace_single_item(1, 0)
        new_board = [
            [None, 'a', 'c'],
            ['c', None, None],
            [None, 'c', 'a']]
        self.assertEqual(self.game.board, new_board)

    def test_1_make_move(self):
        self.game.board = [
            ['c', 'a', 'c'],
            ['b', 'b', 'b'],
            ['b', 'c', 'a']]
        self.game.make_move(2, 0)
        self.assertEqual(self.game.board[2][0], 'c')
        self.assertEqual(self.game.board[2][1], 'c')
        self.assertEqual(self.game.board[2][2], 'a')
        self.assertEqual(self.game.board[1][1], 'a')
        self.assertEqual(self.game.board[1][2], 'c')

    '''TEST COMPLETE GAME CYCLE - 2'''

    def test_2_get_indices_items_to_delete(self):
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', 'a', 'c'],
            ['a', 'a', 'a']]
        correct_indices_items_to_delete = {(2, 0), (2, 1), (2, 2), (1, 1)}
        self.assertEqual(self.game.get_indices_items_to_delete(1, 1), correct_indices_items_to_delete)

    def test_4_delete_items(self):
        indices_items_to_delete = {(2, 0), (2, 1), (2, 2), (1, 1)}
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', 'a', 'c'],
            ['a', 'a', 'a']]
        Game.delete_items(self.game, indices_items_to_delete)
        new_board = [
            ['c', 'b', 'b'],
            ['b', None, 'c'],
            [None, None, None]]
        self.assertEqual(self.game.board, new_board)

    def test_4_replace_items(self):
        indices_items_to_replace = [(2, 2), (2, 1), (2, 0), (1, 1)]
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', None, 'c'],
            [None, None, None]]
        self.game.replace_items(indices_items_to_replace)
        new_board = [
            [None, None, None],
            ['c', None, 'b'],
            ['b', 'b', 'c']]
        self.assertEqual(self.game.board, new_board)

    def test_7_replace_single_item(self):
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', None, 'c'],
            [None, None, None]]
        self.game.replace_single_item(2, 2)
        new_board = [
            ['c', 'b', 'b'],
            ['b', None, None],
            [None, None, 'c']]
        self.assertEqual(self.game.board, new_board)

    def test_8_replace_single_item(self):
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', None, None],
            [None, None, 'c']]
        self.game.replace_single_item(2, 1)
        new_board = [
            ['c', None, 'b'],
            ['b', None, None],
            [None, 'b', 'c']]
        self.assertEqual(self.game.board, new_board)

    def test_9_replace_single_item(self):
        self.game.board = [
            ['c', None, 'b'],
            ['b', None, None],
            [None, 'b', 'c']]
        self.game.replace_single_item(2, 0)
        new_board = [
            ['c', None, 'b'],
            [None, None, None],
            ['b', 'b', 'c']]
        self.assertEqual(self.game.board, new_board)

    def test_10_replace_single_item(self):
        self.game.board = [
            ['c', None, 'b'],
            [None, None, None],
            ['b', 'b', 'c']]
        new_board = self.game.board
        self.game.replace_single_item(1, 1)
        self.assertEqual(self.game.board, new_board)

    def test_2_make_move(self):
        self.game.board = [
            ['c', 'b', 'b'],
            ['b', 'a', 'c'],
            ['a', 'a', 'a']]
        '''new_board = [
            ['x', 'x', 'x'],
            ['c', 'x', 'b'],
            ['b', 'b', 'c']]'''
        self.game.make_move(2, 0)
        self.assertEqual(self.game.board[2][0], 'b')
        self.assertEqual(self.game.board[2][1], 'b')
        self.assertEqual(self.game.board[2][2], 'c')
        self.assertEqual(self.game.board[1][2], 'b')
        self.assertEqual(self.game.board[1][0], 'c')

    def test_3_make_move(self):
        self.game.board = [
            ['a', 'c', 'a'],
            ['a', 'b', 'b'],
            ['a', 'c', 'c']]
        new_board = self.game.board
        self.game.make_move(2, 1)
        self.assertEqual(self.game.board, new_board)

    def test_4_make_move(self):
        self.game.board = [
            ['b', 'c', 'c'],
            ['c', 'c', 'b'],
            ['a', 'a', 'a']]
        '''new_board = [
            ['x', 'x', 'x'],
            ['b', 'c', 'c'],
            ['c', 'c', 'b']]'''
        self.game.make_move(2, 2)
        self.assertEqual(self.game.board[1][0], 'b')
        self.assertEqual(self.game.board[1][1], 'c')
        self.assertEqual(self.game.board[1][2], 'c')
        self.assertEqual(self.game.board[2][0], 'c')
        self.assertEqual(self.game.board[2][1], 'c')
        self.assertEqual(self.game.board[2][2], 'b')

    def test_5_make_move(self):
        self.game.board = [
            ['b', 'c', 'c'],
            ['c', 'c', 'b'],
            ['a', 'a', 'a']]
        '''new_board = [
            ['x', 'x', 'x'],
            ['b', 'c', 'c'],
            ['c', 'c', 'b']]'''
        self.game.make_move(2, 2)
        self.assertEqual(self.game.board[1][0], 'b')
        self.assertEqual(self.game.board[1][1], 'c')
        self.assertEqual(self.game.board[1][2], 'c')
        self.assertEqual(self.game.board[2][0], 'c')
        self.assertEqual(self.game.board[2][1], 'c')
        self.assertEqual(self.game.board[2][2], 'b')

    def test_6_make_move(self):
        self.game.board = [
            ['c', 'a', 'a'],
            ['b', 'b', 'a'],
            ['a', 'b', 'a']]
        old_board = self.game.board
        self.game.make_move(0, 0)
        self.assertFalse(self.game.get_indices_items_to_delete(0, 0))
        self.assertEqual(self.game.board, old_board)
        self.game.make_move(2, 1)
        '''new_board_2 = [
            ['x', 'x', 'a'],
            ['c', 'x', 'a'],
            ['a', 'a', 'a']]'''
        self.assertEqual(self.game.board[1][0], 'c')
        self.assertEqual(self.game.board[1][2], 'a')
        self.assertEqual(self.game.board[2][0], 'a')
        self.assertEqual(self.game.board[2][1], 'a')
        self.assertEqual(self.game.board[2][2], 'a')


if __name__ == '__main__':
    unittest.main()
