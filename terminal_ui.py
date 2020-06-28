from game import Game


class TerminalUI:
    def __init__(self):
        self.game = Game(board_size=3, difficulty_level=1)
        self.game.callback_won_game = self.user_won_game
        self.game.callback_replace_board = self.no_move_move_available
        self.play()

    def play(self):
        self.game.set_up_game()
        while self.game.game_is_running:
            self.make_move()

    def make_move(self):
        self.print_board()
        self.print_score()
        row, column = self.ask_for_move()
        self.game.make_move(row, column)

    def print_board(self, text='This is the current board: '):
        print(text)
        for row in self.game.board:
            print(row)

    def print_score(self):
        print(f'Your target is {self.game.target_score_to_win} points. You currently earned {self.game.score} points.')

    def ask_for_move(self):
        print('Lets make a move... \nPlease enter your row below:')
        row = self.get_input() - 1
        print('Now please enter your column below: ')
        column = self.get_input() - 1
        return row, column

    def get_input(self):
        try:
            input_ = int(input())
            if 0 < input_ <= self.game.board_size:
                return input_
            return self.wrong_input()
        except ValueError:
            return self.wrong_input()

    def wrong_input(self):
        print(f'Please enter a number between 1 and {self.game.board_size}:')
        return self.get_input()

    @staticmethod
    def user_won_game():
        print('Congratulations, you won!')

    def no_move_move_available(self):
        self.game.set_up_board()
        self.print_board('Sorry, no more move! \nThis is your new board: ')


if __name__ == '__main__':
    TerminalUI()

