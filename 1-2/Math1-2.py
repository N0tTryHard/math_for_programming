import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Список цветов для шариков
ball_colors = [
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (255, 255, 0),  # Желтый
    (255, 0, 255),  # Фиолетовый
    (0, 255, 255),  # Голубой
    (255, 165, 0),  # Оранжевый
    (128, 0, 128),  # Пурпурный
    (0, 128, 0),  # Темно-зеленый
    (128, 128, 128)  # Серый
]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Настройки мяча
ball_radius = 25
max_balls = 10

# Список мячей
balls = []


# Функция для рисования мяча
def draw_ball(ball):
    pygame.draw.circle(screen, ball['color'], (ball['x'], ball['y']), ball_radius)


# Функция для создания нового мяча
def create_ball():
    if ball_colors:
        return {
            'x': random.randint(ball_radius, WIDTH - ball_radius),
            'y': random.randint(ball_radius, HEIGHT - ball_radius),
            'speed_x': random.choice([-5, 5]),
            'speed_y': random.choice([-5, 5]),
            'color': ball_colors.pop(0)  # Удаляем использованный цвет из списка
        }
    return None


# Основной цикл игры
running = False
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 75, 100, 50)
stop_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 75, 100, 50)
add_ball_button = pygame.Rect(WIDTH // 2 + 100, HEIGHT - 75, 150, 50)
button_color = WHITE
start_button_text = pygame.font.Font(None, 36).render("Пуск", True, BLACK)
stop_button_text = pygame.font.Font(None, 36).render("Стоп", True, BLACK)
add_ball_button_text = pygame.font.Font(None, 36).render("Добавить", True, BLACK)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos) and not running:
                running = True
                if len(balls) == 0:
                    new_ball = create_ball()
                    if new_ball:
                        balls.append(new_ball)
            elif stop_button.collidepoint(event.pos) and running:
                running = False
            elif add_ball_button.collidepoint(event.pos) and len(balls) < max_balls:
                new_ball = create_ball()
                if new_ball:
                    balls.append(new_ball)

    screen.fill(BLACK)

    if running:
        for ball in balls:
            # Движение мяча
            ball['x'] += ball['speed_x']
            ball['y'] += ball['speed_y']

            # Отскок от границ
            if ball['x'] <= ball_radius or ball['x'] >= WIDTH - ball_radius:
                ball['speed_x'] = -ball['speed_x']
                ball['x'] = max(ball_radius, min(ball['x'], WIDTH - ball_radius))
            if ball['y'] <= ball_radius or ball['y'] >= HEIGHT - ball_radius:
                ball['speed_y'] = -ball['speed_y']
                ball['y'] = max(ball_radius, min(ball['y'], HEIGHT - ball_radius))

            draw_ball(ball)

        # Проверка столкновений между мячами
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                ball1 = balls[i]
                ball2 = balls[j]
                dx = ball1['x'] - ball2['x']
                dy = ball1['y'] - ball2['y']
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < 2 * ball_radius:
                    # Обмен скоростями при столкновении
                    ball1['speed_x'], ball2['speed_x'] = ball2['speed_x'], ball1['speed_x']
                    ball1['speed_y'], ball2['speed_y'] = ball2['speed_y'], ball1['speed_y']

                    # Корректировка позиций, чтобы мячи не слипались
                    overlap = 2 * ball_radius - distance
                    ball1['x'] += dx / distance * overlap / 2
                    ball1['y'] += dy / distance * overlap / 2
                    ball2['x'] -= dx / distance * overlap / 2
                    ball2['y'] -= dy / distance * overlap / 2

        # Отображение кнопки "Стоп"
        pygame.draw.rect(screen, button_color, stop_button)
        screen.blit(stop_button_text, (WIDTH // 2 - 75, HEIGHT - 65))
    else:
        # Отображение кнопки "Пуск"
        pygame.draw.rect(screen, button_color, start_button)
        screen.blit(start_button_text, (WIDTH // 2 - 75, HEIGHT - 65))

    # Отображение кнопки "Добавить мячик"
    pygame.draw.rect(screen, button_color, add_ball_button)
    screen.blit(add_ball_button_text, (WIDTH // 2 + 125, HEIGHT - 65))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
