import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QMessageBox
from game import Game
from PyQt5.QtGui import QPainter, QColor


class CrushUI(QMainWindow):
    def __init__(self):
        super().__init__()
        red = (255, 0, 0)
        yellow = (250, 223, 0)
        light_green = (0, 255, 127)
        navy = (0,0,128)
        blue = 	(0,0,255)
        lavender = (221, 160, 221)
        aqua = (0, 255, 255)
        green = (0, 128, 0)
        maroon = (139, 0, 0)
        game.characters = [aqua, green, light_green, yellow, red, navy, lavender, maroon, blue]
        game.set_up_game()
        self.set_up_widget()

    def set_up_widget(self):
        width, height = 500, 500
        self.resize(width, height)
        board_widget = CrushWidget(self)
        self.setCentralWidget(board_widget)
        self.setWindowTitle('Crush It!')
        self.status_bar = self.statusBar()
        self.refresh_status_bar()
        self.show()
        QMessageBox.information(self, 'Information', 'Crush at least 3 Items!')

    def refresh_status_bar(self):
        self.status_bar.showMessage('Score: {}                   Target: {}'.format(game.score * 10,
                                                                                    game.target * 10))


class CrushWidget(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.set_size()

    def set_size(self):
        self.height = self.parent.frameGeometry().height() - 49
        self.width = self.parent.frameGeometry().width()
        self.square_height = self.height / game.size
        self.square_width = self.width / game.size

    def resizeEvent(self, QResizeEvent):
        self.set_size()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(game.size):
            for column in range(game.size):
                color = game.board[row][column]
                self.paint_square(painter, color, row, column)

    def paint_square(self, painter, color, row, column):
        painter.setBrush(QColor(*color))
        painter.setPen(QColor(255, 255, 255))
        x = self.square_width * column
        y = self.square_height * row
        painter.drawRect(x, y, self.square_width, self.square_height)

    def mousePressEvent(self, event):
        x = int(event.x())
        y = int(event.y())
        row = int(y // self.square_height)
        column = int(x // self.square_width)
        game.play_game(row, column)
        self.parent.refresh_status_bar()
        if game.winner:
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
        else:
            self.update()
            if game.reset_board:
                QMessageBox.information(self.parent, 'no more move',
                                        'Sorry, no more move. \nHere comes your new board!')
                game.set_up_board()
                self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game(10)
    interface = CrushUI()
    sys.exit(app.exec_())
