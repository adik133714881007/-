import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.max_health = 100
        self.exp = 0
        self.level = 1
        self.exp_to_next = 100

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def gain_exp(self, amount):
        self.exp += amount
        # ИСПРАВЛЕНО: Добавлена проверка на прерывание
        if self.exp > self.exp_to_next:
            self.exp = self.exp_to_next

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.exp = 0
        self.exp_to_next = int(self.exp_to_next * 1.5)

    def draw(self, screen, font):
        # Рисуем игрока (маленький кораблик/меч)
        color = (100, 200, 255)

        # Тело игрока
        body_rect = pygame.Rect(self.x - 15, self.y - 20, 30, 40)
        pygame.draw.rect(screen, color, body_rect)
        pygame.draw.rect(screen, (255, 255, 255), body_rect, 2)

        # Оружие (меч/носок)
        weapon_points = [
            (self.x + 15, self.y - 10),
            (self.x + 40, self.y - 5),
            (self.x + 40, self.y + 5),
            (self.x + 15, self.y + 10)
        ]
        pygame.draw.polygon(screen, (200, 200, 255), weapon_points)

        # Глаза
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 5, self.y - 10), 3)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 5, self.y - 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.x - 5, self.y - 10), 1) # ИСПРАВЛЕНО: Добавлены зрачки
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 5, self.y - 10), 1)

        # Полоска здоровья
        health_width = 50
        health_height = 5
        health_x = self.x - health_width // 2
        health_y = self.y - 30

        # Фон здоровья
        pygame.draw.rect(screen, (60, 60, 60), (health_x, health_y, health_width, health_height))

        current_health_width = health_width * (self.health / self.max_health)
        pygame.draw.rect(screen, (255, 80, 80),
                        (health_x, health_y, current_health_width, health_height))