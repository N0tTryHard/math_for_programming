import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
SPACESHIP_SPEED = 5
ROCKET_SPEED = 10
COMET_SPEED = 3
ENERGY_RECOVERY_RATE = 1

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

SCORE_FILE = "./high_scores.txt"


def load_sound(file_name):
    return pygame.mixer.Sound(file_name)


rocket_sound = load_sound("./sounds/odnokratnyiy-piu.mp3")
explosion_sound = load_sound("./sounds/Звук взрыва.mp3")
collision_sound = load_sound("./sounds/Звук столкновения.mp3")
bonus_sound = load_sound("./sounds/бонус.mp3")
movement_sound = load_sound("./sounds/Звук передвижения.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вообще арканоид 2.0")


class Rocket:
    def __init__(self, x):
        self.rect = pygame.Rect(x - 2.5, HEIGHT - 60, 5, 20)

    def move(self):
        self.rect.y -= ROCKET_SPEED

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


class Comet:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 30), -30, 30, 30)

    def move(self):
        self.rect.y += COMET_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)


class Bonus:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 20), -20, 20, 20)

    def move(self):
        self.rect.y += COMET_SPEED

    def draw(self):
        pygame.draw.circle(screen, (255, 215, 0), (self.rect.x + 10, self.rect.y + 10), 10)


class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 30)
        self.energy = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACESHIP_SPEED
            movement_sound.play(-1)
        elif keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += SPACESHIP_SPEED
            movement_sound.play(-1)
        else:
            movement_sound.stop()

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def shoot(self):
        if self.energy > 0:
            rocket_sound.play()
            self.energy -= 1
            return Rocket(self.rect.centerx)
        return None

    def recover_energy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000:
            if self.energy < 5:
                self.energy += ENERGY_RECOVERY_RATE


def load_high_scores():
    if not os.path.exists(SCORE_FILE):
        return []

    with open(SCORE_FILE, 'r') as f:
        scores = [int(line.strip()) for line in f.readlines()]

    return sorted(scores, reverse=True)[:5] if scores else []


def save_high_score(score):
    scores = load_high_scores()

    if len(scores) < 5 or score > min(scores):
        scores.append(score)
        scores.sort(reverse=True)
        if len(scores) > 5:
            scores.pop()

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

    high_scores = load_high_scores()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                rocket = spaceship.shoot()
                if rocket:
                    rockets.append(rocket)

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

        for comet in comets[:]:
            if spaceship.rect.colliderect(comet.rect):
                print("Игра окончена Ваш счет:", score)
                save_high_score(score)
                running = False

            for rocket in rockets[:]:
                if rocket.rect.colliderect(comet.rect):
                    explosion_sound.play()
                    rockets.remove(rocket)
                    comets.remove(comet)
                    score += 5

        for bonus in bonuses[:]:
            if spaceship.rect.colliderect(bonus.rect):
                bonus_sound.play()
                bonuses.remove(bonus)
                spaceship.energy += min(1, (5 - spaceship.energy))

        if random.randint(1, max(20 - score // 10, 5)) == 1:
            comets.append(Comet())

        if random.randint(1, max(50 - score // 20, 10)) == 1:
            bonuses.append(Bonus())

        screen.fill(BLACK)

        spaceship.draw()

        for rocket in rockets:
            rocket.draw()

        for comet in comets:
            comet.draw()

        for bonus in bonuses:
            bonus.draw()

        font = pygame.font.Font(None, 36)

        score_text = font.render(f"Счет: {score}", True, WHITE)
        energy_text = font.render(f"Энергия: {spaceship.energy}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(energy_text, (10, 40))

        high_score_texts = [font.render(f"{i + 1}. {score}", True, WHITE) for i, score in enumerate(high_scores)]

        for i, text in enumerate(high_score_texts):
            screen.blit(text, (WIDTH - text.get_width() - 10, i * text.get_height() + 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
