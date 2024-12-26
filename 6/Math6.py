import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, \
    QMessageBox


def create_field(size):
    return [[' ' for _ in range(size)] for _ in range(size)]


def can_place_ship(field, x, y, size, orientation):
    if orientation == 'horizontal':
        return all(field[x][y + i] == ' ' for i in range(size)) and \
               all(field[nx][ny] == ' ' for nx in range(max(0, x - 1), min(len(field), x + 2)) for ny in
                   range(max(0, y - 1), min(len(field[0]), y + size + 1)))
    else:
        return all(field[x + i][y] == ' ' for i in range(size)) and \
               all(field[nx][ny] == ' ' for nx in range(max(0, x - 1), min(len(field), x + size + 1)) for ny in
                   range(max(0, y - 1), min(len(field[0]), y + 2)))


def mark_neighbors(field, x, y, size, orientation):
    for i in range(size):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if orientation == 'horizontal':
                    nx, ny = x + dx, y + i + dy
                else:
                    nx, ny = x + i + dx, y + dy
                if 0 <= nx < len(field) and 0 <= ny < len(field[0]) and field[nx][ny] != 'S':
                    field[nx][ny] = '*'


def shoot(field, x, y):
    if field[x][y] == 'S':
        field[x][y] = 'X'
        return True
    elif field[x][y] == ' ':
        field[x][y] = 'O'
        return False
    return None


def all_ships_sunk(field):
    return all(cell != 'S' for row in field for cell in row)


def create_3d_field(size):
    return [[[' ' for _ in range(size)] for _ in range(size)] for _ in range(size)]


def can_place_ship_diagonal(field, x, y, size):
    return all(field[x + i][y + i] == ' ' for i in range(size)) and \
           all(field[nx][ny] == ' ' for nx in range(max(0, x - 1), min(len(field), x + size)) for ny in
               range(max(0, y - 1), min(len(field[0]), y + size)))


def place_3d_ships_diagonal(field, num_ships):
    for z in range(len(field)):
        for _ in range(num_ships):
            while True:
                x, y = random.randint(0, len(field[0]) - 2), random.randint(0, len(field[0][0]) - 2)
                if can_place_ship_diagonal(field[z], x, y, 2):
                    field[z][x][y] = 'S'
                    field[z][x + 1][y + 1] = 'S'
                    break


def place_ships(field, ship_sizes):
    for size in ship_sizes:
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                x, y = random.randint(0, len(field) - 1), random.randint(0, len(field[0]) - size)
            else:
                x, y = random.randint(0, len(field) - size), random.randint(0, len(field[0]) - 1)

            if can_place_ship(field, x, y, size, orientation):
                for i in range(size):
                    if orientation == 'vertical':
                        field[x + i][y] = 'S'
                    else:
                        field[x][y + i] = 'S'
                mark_neighbors(field, x, y, size, orientation)
                break


def mark_around_ship(field, x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(field) and 0 <= ny < len(field[0]) and field[nx][ny] == ' ':
                field[nx][ny] = 'O'


class SeaBattle(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.setWindowTitle("Морской бой")
        self.mode = mode
        self.size = 0
        self.player_field = []
        self.computer_field = []
        self.player_display_field = []
        self.computer_display_field = []
        self.player_boxes = []
        self.computer_boxes = []
        self.player_turn = True
        self.last_hit = None
        self.player_last_hit = None
        self.computer_last_hit = None
        self.shot_history = []

        if mode == 1:
            self.player_field = create_field(5)
            self.computer_field = create_field(5)
            place_ships(self.player_field, [2, 2])
            place_ships(self.computer_field, [2, 2])
            self.size = 5
        elif mode == 2:
            self.player_field = create_field(6)
            self.computer_field = create_field(6)
            place_ships(self.player_field, [1, 1, 1])
            place_ships(self.computer_field, [1, 1, 1])
            self.size = 6
        elif mode == 3:
            self.player_field = create_field(7)
            self.computer_field = create_field(7)
            place_ships(self.player_field, [2, 2, 2, 2])
            place_ships(self.computer_field, [2, 2, 2, 2])
            self.size = 7
        elif mode == 4:
            self.player_field_3d = create_3d_field(3)
            self.computer_field_3d = create_3d_field(3)
            place_3d_ships_diagonal(self.player_field_3d, 2)
            place_3d_ships_diagonal(self.computer_field_3d, 2)
            self.size = 3
            self.player_field = self.player_field_3d[0]
            self.computer_field = self.computer_field_3d[0]

        self.player_display_field = create_field(self.size)
        self.computer_display_field = create_field(self.size)

        # Создаем два фрейма для полей
        self.player_frame = QWidget(self)
        self.player_frame.setLayout(QGridLayout())
        self.computer_frame = QWidget(self)
        self.computer_frame.setLayout(QGridLayout())

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.player_frame)
        main_layout.addWidget(self.computer_frame)
        self.setLayout(main_layout)

        self.initialize_game_board(self.player_boxes, self.player_frame, "Игрок")
        self.initialize_game_board(self.computer_boxes, self.computer_frame, "Компьютер")
        self.update_display_board()
        if not self.player_turn:
            self.computer_turn()

    def initialize_game_board(self, picture_boxes, frame, label):
        label = QLabel(label, frame)
        frame.layout().addWidget(label, 0, 0, 1, self.size)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                pb = QPushButton(frame)
                pb.setFixedSize(30, 30)
                pb.setStyleSheet("background-color: lightgray; border: 1px solid black;")
                pb.clicked.connect(lambda _, x=i, y=j: self.picture_box_click(x, y))
                frame.layout().addWidget(pb, i + 1, j)
                row.append(pb)
            picture_boxes.append(row)

    def picture_box_click(self, x, y):
        if self.player_turn:
            if self.computer_display_field[x][y] == ' ':
                result = shoot(self.computer_field, x, y)
                if result:
                    self.computer_display_field[x][y] = 'X'
                    self.player_last_hit = (x, y)
                    self.log_shot(x, y, 'hit', 'player')
                    self.update_display_board()
                    if all_ships_sunk(self.computer_field):
                        QMessageBox.information(self, "Победа", "Вы победили!")
                        self.close()
                else:
                    self.computer_display_field[x][y] = 'O'
                    self.log_shot(x, y, 'miss', 'player')
                    self.update_display_board()
                    self.player_turn = False
                    self.computer_turn()
            else:
                QMessageBox.information(self, "Ошибка", "Эта клетка уже была обстреляна.")

    def computer_turn(self):
        if not self.player_turn:
            hit_occurred = False

            while True:
                if self.computer_last_hit:
                    x, y = self.computer_last_hit
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    random.shuffle(directions)

                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            if self.player_display_field[nx][ny] == ' ':
                                if shoot(self.player_field, nx, ny):
                                    self.player_display_field[nx][ny] = 'X'
                                    self.computer_last_hit = (nx, ny)
                                    hit_occurred = True
                                    self.log_shot(nx, ny, 'hit', 'computer')
                                    self.update_display_board()
                                    if all_ships_sunk(self.player_field):
                                        QMessageBox.information(self, "Поражение", "Вы проиграли!")
                                        self.close()
                                    break
                                else:
                                    self.player_display_field[nx][ny] = 'O'
                                    self.log_shot(nx, ny, 'miss', 'computer')
                                    self.update_display_board()
                                    break

                    if not hit_occurred:
                        self.player_turn = True
                        self.computer_last_hit = None
                        break

                else:
                    x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                    if self.player_display_field[x][y] == ' ':
                        if shoot(self.player_field, x, y):
                            self.player_display_field[x][y] = 'X'
                            self.computer_last_hit = (x, y)
                            self.log_shot(x, y, 'hit', 'computer')
                            self.update_display_board()
                            if all_ships_sunk(self.player_field):
                                QMessageBox.information(self, "Поражение", "Вы проиграли!")
                                self.close()
                        else:
                            self.player_display_field[x][y] = 'O'
                            self.log_shot(x, y, 'miss', 'computer')
                            self.update_display_board()
                            break

            if not hit_occurred and not self.computer_last_hit:
                self.player_turn = True

    def update_display_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.player_field[i][j] == 'S':
                    self.player_boxes[i][j].setStyleSheet("background-color: black;")
                elif self.player_display_field[i][j] == 'X':
                    self.player_boxes[i][j].setStyleSheet("background-color: red;")
                elif self.player_display_field[i][j] == 'O':
                    self.player_boxes[i][j].setStyleSheet("background-color: blue;")
                else:
                    self.player_boxes[i][j].setStyleSheet("background-color: lightgray;")

                if self.computer_display_field[i][j] == 'X':
                    self.computer_boxes[i][j].setStyleSheet("background-color: red;")
                elif self.computer_display_field[i][j] == 'O':
                    self.computer_boxes[i][j].setStyleSheet("background-color: blue;")
                else:
                    self.computer_boxes[i][j].setStyleSheet("background-color: lightgray;")

    def log_shot(self, x, y, result, player):
        self.shot_history.append((x, y, result, player))
        print(f"Shot at ({x}, {y}) by {player}: {result}")


def select_mode():
    mode_window = QWidget()
    mode_window.setWindowTitle("Выбор режима")

    layout = QVBoxLayout()

    def start_mode(mode):
        mode_window.close()
        if mode == 4:
            play_console_mode()
        else:
            game = SeaBattle(mode)
            game.show()

    button1 = QPushButton("Базовый уровень")
    button1.clicked.connect(lambda: start_mode(1))
    layout.addWidget(button1)

    button2 = QPushButton("Средний уровень")
    button2.clicked.connect(lambda: start_mode(2))
    layout.addWidget(button2)

    button3 = QPushButton("Продвинутый уровень")
    button3.clicked.connect(lambda: start_mode(3))
    layout.addWidget(button3)

    button4 = QPushButton("Сложный уровень (консоль)")
    button4.clicked.connect(lambda: start_mode(4))
    layout.addWidget(button4)

    mode_window.setLayout(layout)
    mode_window.show()


def play_console_mode():
    size = 3
    num_ships = 2
    game = SeaBattleConsole(size, num_ships)
    game.play()


class SeaBattleConsole:
    def __init__(self, size, num_ships):
        self.size = size
        self.num_ships = num_ships
        self.player_field = create_3d_field(size)
        self.computer_field = create_3d_field(size)
        self.place_1deck_ships_randomly(self.player_field, num_ships)
        self.place_1deck_ships_randomly(self.computer_field, num_ships)
        self.player_turn = True
        self.computer_shots = []

    def place_1deck_ships_randomly(self, field, num_ships):
        for _ in range(num_ships):
            placed = False
            while not placed:
                z = random.randint(0, self.size - 1)
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if field[z][x][y] == ' ':
                    field[z][x][y] = 'S'
                    placed = True

    def play(self):
        print("Игра началась!")
        while True:
            # Ход игрока
            try:
                x, y, z = map(int, input("Введите координаты выстрела (x y z): ").split())
                if 0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size:
                    if shoot(self.computer_field, x, y):
                        if all_ships_sunk(self.computer_field):
                            print("Победа! Вы потопили все корабли противника.")
                            break
                    else:
                        print("Ваш ход завершён.")
                    # Ход компьютера
                    print("Ход компьютера...")
                    while True:
                        comp_x = random.randint(0, self.size - 1)
                        comp_y = random.randint(0, self.size - 1)
                        comp_z = random.randint(0, self.size - 1)
                        if (comp_x, comp_y, comp_z) not in self.computer_shots:
                            self.computer_shots.append((comp_x, comp_y, comp_z))
                            if shoot(self.player_field, comp_x, comp_y, comp_z):
                                if all_ships_sunk(self.player_field):
                                    print("Поражение! Все ваши корабли потоплены.")
                                    return
                            break
                else:
                    print("Координаты вне диапазона. Попробуйте снова.")
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите три целых числа.")


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    select_mode()
    sys.exit(app.exec_())
