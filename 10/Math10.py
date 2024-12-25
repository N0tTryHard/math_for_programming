import pygame
import random
import math

# Инициализация pygame
pygame.init()

# Параметры окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Гонка по кругу")

# Параметры круга
radius = 200
center_x, center_y = width // 2, height // 2

# Количество участников и кругов
num_participants = 4  # Вы можете изменить это значение на 3-5
num_laps = 3

# Цвета участников (можно изменить на любые другие)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Инициализация участников
participants = []
for i in range(num_participants):
    participants.append({
        'name': f'Персонаж {i + 1}',  # Имя участника
        'position': 0,  # Начальная позиция (угол в радианах)
        'speed': random.uniform(0.01, 0.05),  # Начальная скорость
        'direction': random.choice([1, -1]),  # Направление (1 - вперед, -1 - назад)
        'laps': 0  # Количество пройденных кругов
    })


# Функция для обновления позиции участника
def update_position(participant):
    participant['position'] += participant['speed'] * participant['direction']

    # Проверка на завершение круга: если позиция >= 2π или <= -2π
    if participant['position'] >= 2 * math.pi:
        participant['position'] -= 2 * math.pi
        participant['laps'] += 1
    elif participant['position'] < -2 * math.pi:
        participant['position'] += 2 * math.pi
        participant['laps'] += 1


# Функция для расчета координат участника
def calculate_coordinates(position):
    x = center_x + radius * math.cos(position)
    y = center_y + radius * math.sin(position)
    return int(x), int(y)


# Главный цикл игры
running = True
clock = pygame.time.Clock()
step_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление позиций участников
    for participant in participants:
        update_position(participant)

    # Изменение скорости и направления через каждые 10 шагов
    step_counter += 1
    if step_counter % random.randint(5, 10) == 0:
        for participant in participants:
            participant['speed'] = random.uniform(0.01, 0.05)
            participant['direction'] = random.choice([1, -1])

    # Отображение участников и круга
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 1)

    # Отображение участников и их кругов
    for participant in participants:
        x, y = calculate_coordinates(participant['position'])
        pygame.draw.circle(screen, colors[participants.index(participant)], (x, y), 10)

        font = pygame.font.Font(None, 36)
        text = font.render(f"{participant['name']} - Круги: {participant['laps']}", True, (0, 0, 0))
        screen.blit(text, (x - 50, y - 30))

    # Проверка завершения гонки: если любой участник завершил заданное количество кругов или прошел -3 круга
    if any(participant['laps'] >= num_laps or participant['laps'] <= -3 for participant in participants):
        running = False

    pygame.display.flip()
    clock.tick(30)

# Вывод итоговых позиций в консоль после завершения гонки
print("Итоговые позиции участников:")
for i in sorted(participants, key=lambda p: p['laps'], reverse=True):
    print(f"{i['name']}: {i['laps']} кругов")

pygame.quit()
