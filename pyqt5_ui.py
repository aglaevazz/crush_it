import sys

from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QFrame, QMainWindow, QMessageBox

import colors
from game import Game


class CrushUI(QMainWindow):
    def __init__(self):
        super().__init__()
        game.characters = [colors.aqua, colors.green, colors.light_green, colors.yellow, colors.red, colors.navy,
                           colors.lavender, colors.maroon, colors.blue]
        game.set_up_game()
        self.status_bar = self.statusBar()
        self.set_up_widget()

    def set_up_widget(self):
        width, height = 500, 500
        self.resize(width, height)
        board_widget = CrushWidget(self)
        self.setCentralWidget(board_widget)
        self.setWindowTitle('Crush It!')
        self.refresh_status_bar()
        self.show()
        QMessageBox.information(self, 'Information', 'Crush at least 3 Items!')

    def refresh_status_bar(self):
        self.status_bar.showMessage(f'Score: {game.score * 10}' + str(self.width() // 5 * ' ') +
                                    f'Target: {game.target_score_to_win * 10}')


class CrushWidget(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.square_height = None
        self.square_width = None
        self.set_size()
        game.callback_won_game = self.user_won_game
        game.callback_replace_board = self.no_more_move_available

    def set_size(self):
        self.square_height = self.height() / game.board_size
        self.square_width = self.width() / game.board_size

    def resizeEvent(self, QResizeEvent):
        self.set_size()
        self.update()
        self.parent.refresh_status_bar()

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(game.board_size):
            for column in range(game.board_size):
                color = game.board[row][column]
                self.paint_square(painter, color, row, column)

    def paint_square(self, painter, color, row, column):
        painter.setBrush(QColor(*color))
        painter.setPen(QColor(*colors.white))
        x = self.square_width * column
        y = self.square_height * row
        painter.drawRect(x, y, self.square_width, self.square_height)

    def mousePressEvent(self, event):
        x = int(event.x())
        y = int(event.y())
        row = int(y // self.square_height)
        column = int(x // self.square_width)
        game.make_move(row, column)
        self.parent.refresh_status_bar()
        self.update()

    def user_won_game(self):
        QMessageBox.information(self.parent, 'Winner!', 'Congratulations, You Won!')
        play_again_message_box = QMessageBox(self)
        play_again_answer = play_again_message_box.question(self.parent,
                                                            'Winner!', 'Do you want to Crush-It again?',
                                                            play_again_message_box.Yes | play_again_message_box.No,
                                                            play_again_message_box.Yes)
        if play_again_answer == QMessageBox.No:
            sys.exit()
        else:
            game.set_up_game()
            self.parent.refresh_status_bar()
            self.parent.board_widget = CrushWidget(self.parent)

    def no_more_move_available(self):
        QMessageBox.information(self.parent, 'no more move',
                                'Sorry, no more move. \nHere comes your new board!')
        game.set_up_board()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game(10)
    interface = CrushUI()
    sys.exit(app.exec_())
