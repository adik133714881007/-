import pygame

class Enemy:
    def __init__(self, word, x, y, colors):
        self.word = word
        self.word_length = len(word)
        self.x = x
        self.y = y
        self.colors = colors
        self.speed = 30 + self.word_length * 5  # Пикселей в секунду
        self.width = len(word) * 15 + 20
        self.height = 40
        self.health = 100  # Добавлено здоровье врага
        self.max_health = 100

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen, font):
        # Внешний вид врага
        color = self.colors['enemy']

        # Тело врага
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, color, enemy_rect)
        pygame.draw.rect(screen, (255, 255, 255), enemy_rect, 2)

        # Глаза врага
        eye_y = self.y + 10
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x + 10), int(eye_y)), 5)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x + self.width - 10), int(eye_y)), 5)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 10), int(eye_y)), 2)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.width - 10), int(eye_y)), 2)

        # Текст врага (слово)
        text_surface = font.render(self.word, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.x + self.width/2), int(self.y + self.height/2)))
        screen.blit(text_surface, text_rect)

        # Полоса здоровья врага
        health_width = self.width - 10
        health_height = 5
        health_x = self.x + 5
        health_y = self.y - 10
        
        # Текущее здоровье в процентах
        current_health_width = int(health_width * (self.health / self.max_health))

        # Фон полосы здоровья
        pygame.draw.rect(screen, (60, 60, 60), (health_x, health_y, health_width, health_height))
        # Активная полоса здоровья
        pygame.draw.rect(screen, (255, 100, 100), (health_x, health_y, current_health_width, health_height))

    def take_damage(self, damage):
        """Уменьшает здоровье врага при получении урона"""
        self.health -= damage
        return self.health <= 0  # Возвращает True, если враг мертв

    def is_off_screen(self):
        """Проверяет, ушел ли враг за левый край экрана"""
        return self.x + self.width < 0