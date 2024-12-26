import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt

# Размеры окна
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Лабиринт
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
]

# Координаты игрока
player_x, player_y = 0, 1


class MazeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(WIDTH, HEIGHT)

    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(ROWS):
            for x in range(COLS):
                color = QColor(0, 0, 0) if maze[y][x] == 1 else QColor(255, 255, 255)
                painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QBrush(color))
        painter.fillRect(player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QBrush(QColor(0, 0, 255)))
        painter.fillRect(8 * CELL_SIZE, 9 * CELL_SIZE, CELL_SIZE, CELL_SIZE, QBrush(QColor(0, 255, 0)))


class PathWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(WIDTH, HEIGHT)

    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 3:
                    painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QBrush(QColor(255, 0, 0)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Прародитель лабиринта")
        self.setGeometry(100, 100, WIDTH * 2 + 20, HEIGHT)

        self.maze_widget = MazeWidget(self)
        self.path_widget = PathWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.maze_widget)
        layout.addWidget(self.path_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        global player_x, player_y
        new_x, new_y = player_x, player_y
        if event.key() == Qt.Key_Up:
            new_y -= 1
        elif event.key() == Qt.Key_Down:
            new_y += 1
        elif event.key() == Qt.Key_Left:
            new_x -= 1
        elif event.key() == Qt.Key_Right:
            new_x += 1

        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] != 1:
            maze[player_y][player_x] = 3
            player_x, player_y = new_x, new_y

        self.maze_widget.update()
        self.path_widget.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
