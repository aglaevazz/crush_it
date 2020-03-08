from game import Game


class TerminalUI:
    def __init__(self):
        self.play()

    def play(self):
        game.set_up_game()
        self.print_board()
        while not game.winner:
            self.make_move()
        print('You won!')

    def make_move(self):
        self.print_score()
        row, column = self.ask_for_move()
        game.play_game(row, column)
        self.print_board()
        if game.reset_board:
            game.set_up_board()
            self.print_board('Sorry, no more move! \nThis is your new board: ')

    @staticmethod
    def print_board(text='This is the current board: '):
        print(text)
        for row in game.board:
            print(row)

    @staticmethod
    def print_score():
        print('Your target is {} points. You currently earned {} points.'.format(game.target, game.score))

    @staticmethod
    def ask_for_move():
        print('Lets make a move... \nPlease enter your row below:')
        row = int(input())
        print('Now please enter your column below: ')
        column = int(input())
        return row, column


if __name__ == '__main__':
    game = Game(3, target=10)
    TerminalUI()

