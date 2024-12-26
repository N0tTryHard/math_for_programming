import pygame
import random
from collections import deque

# Константы
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)


# Определение типов препятствий
class Obstacle:
    def __init__(self, symbol):
        self.symbol = symbol


class SlowObstacle(Obstacle):
    def __init__(self):
        super().__init__('S')


class DangerousObstacle(Obstacle):
    def __init__(self):
        super().__init__('D')


class TeleportObstacle(Obstacle):
    def __init__(self):
        super().__init__('T')


class FreezeObstacle(Obstacle):
    def __init__(self):
        super().__init__('F')


# Определение класса игрока
class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_frozen = False
        self.steps = 0

    def move(self, direction, maze):
        if self.is_frozen:
            return

        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])

        if maze.is_valid_move(new_position):
            self.position = new_position
            self.steps += 1
            maze.check_obstacle(self)


# Определение класса лабиринта
class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.start = (1, 1)  # Начальная позиция игрока
        self.exit = (len(layout) - 2, len(layout[0]) - 2)  # Выход в центре лабиринта

    def is_valid_move(self, position):
        x, y = position
        return (0 <= x < len(self.layout) and
                0 <= y < len(self.layout[0]) and
                self.layout[x][y] != 'X')  # 'X' - стена

    def check_obstacle(self, player):
        x, y = player.position
        cell = self.layout[x][y]

        if cell == 'S':
            player.steps += 2  # Замедление на 2 шага
        elif cell == 'D':
            player.position = (1, 1)  # Возврат к старту
            player.steps += 1
        elif cell == 'T':
            player.position = random.choice([(1, 1), (1, 2), (2, 1)])  # Телепортация в случайную клетку
            player.steps += 1
        elif cell == 'F':
            player.is_frozen = True

    def find_path(self, start, end):
        queue = deque([start])
        visited = set()
        visited.add(start)
        path = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                break
            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_position = (current[0] + direction[0], current[1] + direction[1])
                if self.is_valid_move(new_position) and new_position not in visited:
                    queue.append(new_position)
                    visited.add(new_position)
                    path[new_position] = current

        return path

    def get_ideal_steps(self):
        path = self.find_path(self.start, self.exit)
        steps = 0
        current = self.exit
        while current:
            steps += 1
            current = path[current]
        return steps - 1  # Исключаем начальную позицию


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра в лабиринт")

# Лабиринт и игроки (большой замкнутый лабиринт)
layout = [
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
    ['X', ' ', 'X', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X'],
    ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
    ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
    ['X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X'],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
]

# Добавление препятствий
layout[2][2] = 'S'
layout[4][4] = 'D'
layout[6][6] = 'T'
layout[8][8] = 'F'
layout[10][10] = 'S'
layout[12][12] = 'D'
layout[14][14] = 'T'
layout[12][14] = 'F'
layout[2][14] = 'S'
layout[4][12] = 'D'
layout[6][10] = 'T'
layout[8][6] = 'F'
layout[10][4] = 'S'
layout[12][2] = 'D'
layout[14][10] = 'T'
layout[12][8] = 'F'
layout[3][3] = 'S'
layout[5][5] = 'D'
layout[7][7] = 'T'
layout[9][9] = 'F'
layout[11][11] = 'S'
layout[13][13] = 'D'
layout[13][15] = 'F'

# Выход
layout[14][18] = 'E'

maze = Maze(layout)
player1 = Player("Игрок 1", maze.start)
player2 = Player("Игрок 2", maze.start)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

# Найти идеальный путь для Игрока 2
ideal_path = maze.find_path(maze.start, maze.exit)
ideal_path_steps = []
current = maze.exit
while current:
    ideal_path_steps.append(current)
    current = ideal_path[current]
ideal_path_steps.reverse()

while running:
    screen.fill(WHITE)  # Фон белый

    # Отрисовка окантовки вокруг игрового поля
    pygame.draw.rect(screen, BLACK, (2, 2, WIDTH - 4, HEIGHT - 4), 5)

    # Отрисовка лабиринта и игроков
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            cell_x = j * GRID_SIZE + (WIDTH - COLS * GRID_SIZE) // 2
            cell_y = i * GRID_SIZE + (HEIGHT - ROWS * GRID_SIZE) // 2

            if layout[i][j] == 'X':
                pygame.draw.rect(screen, BLACK, (cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
            elif layout[i][j] == 'S':
                pygame.draw.rect(screen, YELLOW, (cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
            elif layout[i][j] == 'D':
                pygame.draw.rect(screen, RED, (cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
            elif layout[i][j] == 'T':
                pygame.draw.rect(screen, BLUE, (cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
            elif layout[i][j] == 'F':
                pygame.draw.rect(screen, GREEN, (cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2))
            elif layout[i][j] == 'E':
                pygame.draw.rect(screen, PURPLE, (cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2))

            if (i, j) == player1.position:
                pygame.draw.circle(screen,
                                   GREEN if not player1.is_frozen else BLACK,
                                   (cell_x + GRID_SIZE // 2, cell_y + GRID_SIZE // 2), GRID_SIZE // 3)

            if (i, j) == player2.position:
                pygame.draw.circle(screen,
                                   BLUE if not player2.is_frozen else BLACK,
                                   (cell_x + GRID_SIZE // 2, cell_y + GRID_SIZE // 2), GRID_SIZE // 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Ход игрока 1 (пользовательский ввод)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.move((-1, 0), maze)
            elif event.key == pygame.K_s:
                player1.move((1, 0), maze)
            elif event.key == pygame.K_a:
                player1.move((0, -1), maze)
            elif event.key == pygame.K_d:
                player1.move((0, 1), maze)

    # Ход игрока 2 (автоматический поиск пути)
    if not player2.is_frozen and ideal_path_steps:
        next_move = ideal_path_steps.pop(0)
        direction = (next_move[0] - player2.position[0], next_move[1] - player2.position[1])
        player2.move(direction, maze)

    # Проверка на победу
    if player1.position == maze.exit:
        print(f"Игрок 1 победил за {player1.steps} ходов!")
        running = False
    elif player2.position == maze.exit:
        print(f"Игрок 2 победил за {player2.steps} ходов!")
        running = False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
