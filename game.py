import random
import string


class Game:
    def __init__(self, size=3, characters=string.ascii_letters, target=100):
        self.size = size
        self.characters = characters[:self.size - 1]
        self.target = target
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def set_up_game(self):
        self.set_values()
        self.score = 0
        self.winner = False
        self.set_up_board()

    def set_values(self):
        self.delete = set()
        self.create_items = []

    def play_game(self, row, column):
        if self.winner:
            return
        self.set_values()
        self.make_move(row, column)
        if self.no_next_move():
            return 'no more move'

    def set_up_board(self):
        for row in range(self.size):
            for column in range(self.size):
                character = random.choice(self.characters)
                self.board[row][column] = character
        if self.no_next_move():
            self.set_up_board()

    def make_move(self, row, column):
        self.check_move(row, column)
        if len(self.delete) < 3:
            return
        self.delete_items()
        self.replace_items()
        self.create_new_items()
        if self.score >= self.target:
            self.winner = True

    def check_move(self, row, column):
        current_item = self.board[row][column]
        current_item_coordinates = row, column
        neighbor_items = self.neighbor_items(row, column)
        neighbor_coordinates = self.neighbor_coordinates(row, column)
        for next_item, next_item_coordinates in zip(neighbor_items, neighbor_coordinates):
            if current_item == next_item:
                self.delete.add(current_item_coordinates)
                if next_item_coordinates not in self.delete:
                    self.check_move(*next_item_coordinates)

    def no_next_move(self):
        for row in range(self.size):
            for column in range(self.size):
                self.check_move(row, column)
                equal_neighbors = self.delete
                self.delete = set()
                if len(equal_neighbors) >= 3:
                    return False
        return True

    def neighbor_items(self, row, column):
        left, right, lower, upper = None, None, None, None
        if column > 0:
            left = self.board[row][column - 1]
        if column < self.size - 1:
            right = self.board[row][column + 1]
        if row < self.size - 1:
            lower = self.board[row + 1][column]
        if row > 0:
            upper = self.board[row - 1][column]
        return [left, right, lower, upper]

    def neighbor_coordinates(self, row, column):
        left, right, lower, upper = None, None, None, None
        if column > 0:
            left = row, column - 1
        if column < self.size - 1:
            right = row, column + 1
        if row < self.size - 1:
            lower = row + 1, column
        if row > 0:
            upper = row - 1, column
        return [left, right, lower, upper]

    @staticmethod
    def row_above(row):
        if row > 0:
            return True
        return False

    def delete_items(self):
        for item in self.delete:
            row = item[0]
            column = item[1]
            self.board[row][column] = None
            self.score += 1
        self.replace = list(sorted(self.delete, reverse=True))

    def switch_items(self, lower_row, lower_column, upper_row, upper_column):
        upper_item = self.board[upper_row][upper_column]
        self.board[lower_row][lower_column] = upper_item
        self.board[upper_row][upper_column] = None

    def replace_items(self):
        if self.replace:
            row, column = self.replace[0]
            if self.row_above(row):
                self.replace_single_item(row, column)
            else:
                self.create_items.append((row, column))
            self.replace = self.replace[1:]
            self.replace_items()

    def replace_single_item(self, row, column):
        current_coordinates = row, column
        upper_item_row, upper_item_column = row - 1, column
        upper_item = self.board[upper_item_row][upper_item_column]
        while not upper_item and self.row_above(upper_item_row):
            upper_item_row = upper_item_row - 1
            upper_item = self.board[upper_item_row][upper_item_column]
        if upper_item:
            self.switch_items(*current_coordinates, upper_item_row, upper_item_column)
            self.replace.append((upper_item_row, upper_item_column))
        else:
            self.create_items.append(current_coordinates)

    def create_new_items(self):
        for coordinate in self.create_items:
            row, column = coordinate
            self.board[row][column] = random.choice(self.characters)


