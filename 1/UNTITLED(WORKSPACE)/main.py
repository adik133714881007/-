import pygame
import sys
from game import Game

def main():
    pygame.init()
    pygame.display.set_caption("Type & Slayer - Рогалик ☠ печать")

    # Настройки экрана
    screen_info = pygame.display.Info()
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Создание игры
    game = Game(screen, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Основной цикл
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Дельта времени в секундах

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()