import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
SPACESHIP_SPEED = 5
ROCKET_SPEED = 10
COMET_SPEED = 3

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Создание окна игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Типа арканоид")


# Класс для звездолета
class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 30)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACESHIP_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += SPACESHIP_SPEED

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


# Класс для ракет
class Rocket:
    def __init__(self, x):
        self.rect = pygame.Rect(x - 2.5, HEIGHT - 60, 5, 20)

    def move(self):
        self.rect.y -= ROCKET_SPEED

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


# Класс для комет
class Comet:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30)

    def move(self):
        self.rect.y += COMET_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    rockets = []
    comets = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Стрельба ракетами
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(rockets) < 5:
                    rockets.append(Rocket(spaceship.rect.centerx))

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
                score += 1

        # Проверка столкновений
        for comet in comets[:]:
            if spaceship.rect.colliderect(comet.rect):
                print("Игра окончена! Ваш счет:", score)
                running = False

            for rocket in rockets[:]:
                if rocket.rect.colliderect(comet.rect):
                    rockets.remove(rocket)
                    comets.remove(comet)
                    score += 5

        # Добавление новых комет
        if random.randint(1, 20) == 1:
            comets.append(Comet())

        # Отрисовка объектов на экране
        screen.fill(BLACK)
        spaceship.draw()

        for rocket in rockets:
            rocket.draw()

        for comet in comets:
            comet.draw()

        # Отображение счета на экране
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
