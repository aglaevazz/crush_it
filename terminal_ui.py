from game import Game


class TerminalUI:
    def __init__(self):
        self.play()

    def play(self):
        game.set_up_game()
        while not game.winner:
            self.make_move()
        print('You won!')

    def make_move(self):
        self.print_board()
        self.print_score()
        row, column = self.ask_for_move()
        result = game.play_game(row, column)
        if result == 'no more move':
            game.set_up_board()
            self.print_board('Sorry, no more move! \nThis is your new board: ')

    @staticmethod
    def print_board(text='This is the current board: '):
        print(text)
        for row in game.board:
            print(row)

    @staticmethod
    def print_score():
        print(f'Your target is {game.target} points. You currently earned {game.score} points.')

    def ask_for_move(self):
        print('Lets make a move... \nPlease enter your row below:')
        row = self.get_input() - 1
        print('Now please enter your column below: ')
        column = self.get_input() - 1
        return row, column

    def get_input(self):
        try:
            input_ = int(input())
            if 0 < input_ <= game.size:
                return input_
            return self.wrong_input()
        except ValueError:
            return self.wrong_input()

    def wrong_input(self):
        print(f'Please enter a number between 1 and {game.size}:')
        return self.get_input()


if __name__ == '__main__':
    game = Game(3, target=10)
    TerminalUI()

