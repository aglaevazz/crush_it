import random
import string


class Game:
    def __init__(self, board_size=3, difficulty_level='medium'):
        self.board_size = board_size
        self.difficulty_level = difficulty_level
        self.target_score_to_win = None
        self.score = None
        self.game_is_running = True
        self.characters = string.ascii_letters
        self.board = [[None] * self.board_size for _ in range(board_size)]
        self.callback_won_game = None
        self.callback_replace_board = None

    def set_up_game(self):
        self.set_difficulty_level()
        self.score = 0
        self.game_is_running = True
        self.set_up_board()

    def set_difficulty_level(self):
        if self.difficulty_level == 'easy':
            self.characters = self.characters[:self.board_size - self.board_size // 2]
            self.target_score_to_win = 20
        elif self.difficulty_level == 'medium':
            self.characters = self.characters[:self.board_size - self.board_size // 3]
            self.target_score_to_win = 50
        elif self.difficulty_level == 'hard':
            self.characters = self.characters[:self.board_size]
            self.target_score_to_win = 100

    def set_up_board(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                character = random.choice(self.characters)
                self.board[row][column] = character
        if not self.next_move_is_available():
            self.set_up_board()

    def make_move(self, row, column):
        indices_items_to_delete = self.get_indices_items_to_delete(row, column)
        if len(indices_items_to_delete) < 3:
            return
        self.delete_items(indices_items_to_delete)
        indices_create_new_items = self.replace_items(list(sorted(indices_items_to_delete, reverse=True)))
        self.create_new_items(indices_create_new_items)
        if self.score >= self.target_score_to_win:
            self.game_is_running = False
            if self.callback_won_game:
                self.callback_won_game()
        if not self.next_move_is_available() and self.callback_replace_board:
            self.callback_replace_board()

    def get_indices_items_to_delete(self, row, column, indices_items_to_delete=None):
        if not indices_items_to_delete:
            indices_items_to_delete = set()
        current_item = self.board[row][column]
        current_item_coordinates = row, column
        neighbor_items = self.get_neighbor_items(row, column)
        neighbor_coordinates = self.get_neighbor_coordinates(row, column)
        for next_item, next_item_coordinates in zip(neighbor_items, neighbor_coordinates):
            if current_item == next_item and next_item_coordinates:
                indices_items_to_delete.add(current_item_coordinates)
                if next_item_coordinates not in indices_items_to_delete:
                    self.get_indices_items_to_delete(*next_item_coordinates, indices_items_to_delete)
        return indices_items_to_delete

    def next_move_is_available(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                if len(self.get_indices_items_to_delete(row, column)) >= 3:
                    return True
        return False

    def get_neighbor_items(self, row, column):
        left, right, lower, upper = None, None, None, None
        if column > 0:
            left = self.board[row][column - 1]
        if column < self.board_size - 1:
            right = self.board[row][column + 1]
        if row < self.board_size - 1:
            lower = self.board[row + 1][column]
        if row > 0:
            upper = self.board[row - 1][column]
        return [left, right, lower, upper]

    def get_neighbor_coordinates(self, row, column):
        left, right, lower, upper = None, None, None, None
        if column > 0:
            left = row, column - 1
        if column < self.board_size - 1:
            right = row, column + 1
        if row < self.board_size - 1:
            lower = row + 1, column
        if row > 0:
            upper = row - 1, column
        return [left, right, lower, upper]

    @staticmethod
    def there_is_row_above(row):
        if row > 0:
            return True
        return False

    def delete_items(self, indices_items_to_delete):
        for index in indices_items_to_delete:
            row, column = index
            self.board[row][column] = None
            self.score += 1

    def swap_items(self, lower_row, lower_column, upper_row, upper_column):
        upper_item = self.board[upper_row][upper_column]
        self.board[lower_row][lower_column] = upper_item
        self.board[upper_row][upper_column] = None

    def replace_items(self, indices_items_to_replace, indices_create_new_items=None):
        if not indices_create_new_items:
            indices_create_new_items = []
        if indices_items_to_replace:
            row, column = indices_items_to_replace[0]
            if self.there_is_row_above(row):
                request, coordinates = self.replace_single_item(row, column)
                if request == 'replace item':
                    indices_items_to_replace.append(coordinates)
                elif request == 'create new item':
                    indices_create_new_items.append(coordinates)
            else:
                indices_create_new_items.append((row, column))
            return self.replace_items(indices_items_to_replace[1:], indices_create_new_items)
        return indices_create_new_items

    def replace_single_item(self, row, column):
        current_coordinates = row, column
        upper_item_row, upper_item_column = row - 1, column
        upper_item = self.board[upper_item_row][upper_item_column]
        while not upper_item and self.there_is_row_above(upper_item_row):
            upper_item_row = upper_item_row - 1
            upper_item = self.board[upper_item_row][upper_item_column]
        if upper_item:
            self.swap_items(*current_coordinates, upper_item_row, upper_item_column)
            return 'replace item', (upper_item_row, upper_item_column)
        else:
            return 'create new item', current_coordinates

    def create_new_items(self, indices_create_new_items):
        for coordinate in indices_create_new_items:
            row, column = coordinate
            self.board[row][column] = random.choice(self.characters)
