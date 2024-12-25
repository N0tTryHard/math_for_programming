import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

# Определяем размеры клетки и размеры окна
CELL_SIZE = 40
MAZE_WIDTH = 10
MAZE_HEIGHT = 10

# Определяем лабиринт
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

# Начальные координаты игрока (можно изменить на любую допустимую позицию)
player_x = player_y = (5, 5)  # Начинаем с позиции (5,5), которая свободна


class MazeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path_points = []  # Список для хранения пройденного пути
        self.path_points.append(player_x)  # Добавляем начальную позицию в путь

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_maze(painter)
        self.draw_path(painter)

    def draw_maze(self, painter):
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == 1:
                    painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QColor("black"))  # Стена
                elif (x == player_x[0] and y == player_x[1]):
                    painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QColor("blue"))  # Игрок

    def draw_path(self, painter):
        for point in self.path_points:
            x, y = point
            painter.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QColor("red"))  # Пройденный путь


class MazeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maze Game")
        self.setGeometry(100, 100, MAZE_WIDTH * CELL_SIZE * 2, MAZE_HEIGHT * CELL_SIZE)

        self.maze_widget = MazeWidget(self)
        self.setCentralWidget(self.maze_widget)

    def keyPressEvent(self, event):
        global player_x
        new_x = player_x[0]
        new_y = player_x[1]

        if event.key() == Qt.Key_Up:
            new_y -= 1
        elif event.key() == Qt.Key_Down:
            new_y += 1
        elif event.key() == Qt.Key_Left:
            new_x -= 1
        elif event.key() == Qt.Key_Right:
            new_x += 1

        # Проверка на допустимость нового положения
        if (0 <= new_x < len(maze[0]) and
                0 <= new_y < len(maze) and
                maze[new_y][new_x] == 0):
            player_x = (new_x, new_y)

            # Добавляем новую позицию в список пройденного пути
            if player_x not in self.maze_widget.path_points:
                self.maze_widget.path_points.append(player_x)

        self.maze_widget.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = MazeGame()
    game.show()
    sys.exit(app.exec_())
