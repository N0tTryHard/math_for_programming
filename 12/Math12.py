import pygame
import os
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
SPACESHIP_SPEED = 5
ROCKET_SPEED = 10
COMET_SPEED = 3
ENERGY_RECOVERY_RATE = 1  # Энергия восстанавливается на 1 единицу за секунду

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Файл для хранения рекордов
SCORE_FILE = "./high_scores.txt"


# Функция для загрузки звуковых эффектов
def load_sound(file_name):
    return pygame.mixer.Sound(file_name)


# Звуковые эффекты (файлы должны находиться в той же директории)
rocket_sound = load_sound("./sounds/odnokratnyiy-piu.mp3")  # Звук запуска ракеты
explosion_sound = load_sound("./sounds/Звук взрыва.mp3")  # Звук взрыва кометы или ракеты
collision_sound = load_sound(
    "./sounds/Звук столкновения.mp3")  # Звук столкновения (если хотите добавить)
bonus_sound = load_sound("./sounds/бонус.mp3")  # Звук получения бонуса
movement_sound = load_sound("./sounds/Звук передвижения.mp3")  # Звук работы двигателя

# Создание окна игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звездолет против комет")


# Класс для ракет
class Rocket:
    def __init__(self, x):
        self.rect = pygame.Rect(x - 2.5, HEIGHT - 60, 5, 20)  # Позиция ракеты

    def move(self):
        self.rect.y -= ROCKET_SPEED  # Движение ракеты вверх

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)  # Отрисовка ракеты


# Класс для комет
class Comet:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 30), -30, 30, 30)  # Позиция кометы

    def move(self):
        self.rect.y += COMET_SPEED  # Движение кометы вниз

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)  # Отрисовка кометы


# Класс для бонусов
class Bonus:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 20), -20, 20, 20)  # Позиция бонуса

    def move(self):
        self.rect.y += COMET_SPEED  # Движение бонуса вниз

    def draw(self):
        pygame.draw.circle(screen, (255, 215, 0), (self.rect.x + 10, self.rect.y + 10), 10)  # Отрисовка бонуса


# Класс для звездолета
class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 30)
        self.energy = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACESHIP_SPEED
            movement_sound.play(-1)  # Воспроизведение звука работы двигателя в цикле при движении влево
        elif keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += SPACESHIP_SPEED
            movement_sound.play(-1)  # Воспроизведение звука работы двигателя в цикле при движении вправо
        else:
            movement_sound.stop()  # Остановка звука при отсутствии движения

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def shoot(self):
        if self.energy > 0:
            rocket_sound.play()  # Воспроизведение звука запуска ракеты
            self.energy -= 1
            return Rocket(self.rect.centerx)
        return None

    def recover_energy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000:  # Восстановление энергии каждую секунду
            if self.energy < 5:
                self.energy += ENERGY_RECOVERY_RATE


def load_high_scores():
    """Загрузка таблицы рекордов из файла."""
    if not os.path.exists(SCORE_FILE):
        return []

    with open(SCORE_FILE, 'r') as f:
        scores = [int(line.strip()) for line in f.readlines()]

    return sorted(scores, reverse=True)[:5] if scores else []


def save_high_score(score):
    """Сохранение нового рекорда в файл."""
    scores = load_high_scores()

    if len(scores) < 5 or score > min(scores):
        scores.append(score)
        scores.sort(reverse=True)  # Сортировка по убыванию

        if len(scores) > 5:
            scores.pop()  # Удаляем самый низкий рекорд

        with open(SCORE_FILE, 'w') as f:
            for s in scores:
                f.write(f"{s}\n")


def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    rockets = []
    comets = []
    bonuses = []
    score = 0

    high_scores = load_high_scores()  # Загружаем таблицу рекордов

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Стрельба ракетами
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                rocket = spaceship.shoot()
                if rocket:
                    rockets.append(rocket)

        # Движение объектов
        spaceship.move()

        for rocket in rockets[:]:
            rocket.move()
            if rocket.rect.bottom < 0:
                rockets.remove(rocket)

        for comet in comets[:]:
            comet.move()
            if comet.rect.top > HEIGHT:
                comets.remove(comet)

        for bonus in bonuses[:]:
            bonus.move()
            if bonus.rect.top > HEIGHT:
                bonuses.remove(bonus)

        # Проверка столкновений с кометами и бонусами
        for comet in comets[:]:
            if spaceship.rect.colliderect(comet.rect):
                print("Игра окончена! Ваш счет:", score)
                save_high_score(score)  # Сохраняем счет в таблицу рекордов перед выходом из игры
                running = False

            for rocket in rockets[:]:
                if rocket.rect.colliderect(comet.rect):
                    explosion_sound.play()  # Воспроизведение звука взрыва при уничтожении кометы
                    rockets.remove(rocket)
                    comets.remove(comet)
                    score += 5  # Увеличиваем счет за уничтожение кометы

        for bonus in bonuses[:]:
            if spaceship.rect.colliderect(bonus.rect):
                bonus_sound.play()  # Воспроизведение звука получения бонуса
                bonuses.remove(bonus)
                spaceship.energy += min(1, (5 - spaceship.energy))  # Восстановление энергии при получении бонуса

        # Добавление новых объектов с динамическим управлением уровнями сложности
        if random.randint(1,
                          max(20 - score // 10, 5)) == 1:  # Уменьшение времени появления комет по мере увеличения счета
            comets.append(Comet())

        if random.randint(1, max(50 - score // 20,
                                 10)) == 1:  # Уменьшение времени появления бонусов по мере увеличения счета
            bonuses.append(Bonus())

        # Отрисовка объектов на экране
        screen.fill(BLACK)

        spaceship.draw()

        for rocket in rockets:
            rocket.draw()

        for comet in comets:
            comet.draw()

        for bonus in bonuses:
            bonus.draw()

        # Отображение счета и энергии на экране и таблицы рекордов
        font = pygame.font.Font(None, 36)

        score_text = font.render(f"Счет: {score}", True, WHITE)
        energy_text = font.render(f"Энергия: {spaceship.energy}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(energy_text, (10, 40))

        # Отображение таблицы рекордов на экране
        high_score_texts = [font.render(f"{i + 1}. {score}", True, WHITE) for i, score in enumerate(high_scores)]

        for i, text in enumerate(high_score_texts):
            screen.blit(text, (WIDTH - text.get_width() - 10, i * text.get_height() + 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
