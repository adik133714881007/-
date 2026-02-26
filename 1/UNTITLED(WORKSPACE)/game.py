import pygame
import random
from entities.player import Player
from entities.enemy import Enemy
from entities.keyboard import VirtualKeyboard
from utils.word_generator import WordGenerator

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        
        # Цвета
        self.colors = {
            'background': (20, 20, 30),
            'text': (255, 255, 255),
            'enemy': (255, 100, 100),
            'enemy_hover': (255, 150, 150),
            'ui': (50, 50, 70),
            'health': (255, 80, 80),
            'exp': (100, 255, 100),
            'keyboard_bg': (30, 30, 40),
            'key_normal': (60, 60, 80),
            'key_pressed': (100, 100, 150),
            'key_special': (80, 80, 120),
        }
        
        # Игровые объекты
        self.player = Player(50, height // 2)
        self.word_generator = WordGenerator()
        self.enemies = []
        self.keyboard = VirtualKeyboard(50, height - 220, self.colors)
        
        # Игровые параметры
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        self.spawn_delay = 2.0  # Секунды между спавном
        self.current_word = ""
        self.typed_word = ""
        
        # Шрифты
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 48)
        self.main_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Статус игры
        self.game_over = False
        self.victory = False
        
    def handle_event(self, event):
        if self.game_over or self.victory:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            return
            
        if event.type == pygame.KEYDOWN:
            # Обработка ввода
            if event.key == pygame.K_BACKSPACE:
                self.typed_word = self.typed_word[:-1]
                self.keyboard.press_key('backspace')
            elif event.key == pygame.K_RETURN:
                self.check_word()
                self.keyboard.press_key('enter')
            elif event.key == pygame.K_ESCAPE:
                self.typed_word = ""
            else:
                # Добавляем символ, если это буква
                char = event.unicode.lower()
                if char.isalpha():
                    self.typed_word += char
                    self.keyboard.press_key(char)
                    
    def check_word(self):
        """Проверка введенного слова"""
        for enemy in self.enemies[:]:
            if enemy.word == self.typed_word:
                self.enemies.remove(enemy)
                self.score += enemy.word_length * 10
                self.player.gain_exp(10)
                self.typed_word = ""
                return
        # Если слово не найдено
        self.typed_word = ""
        
    def spawn_enemy(self):
        """Создание нового врага"""
        if len(self.enemies) < 5 + self.level * 2:
            word = self.word_generator.get_random_word(self.level)
            x = self.width
            y = random.randint(100, self.height - 300)
            enemy = Enemy(word, x, y, self.colors)
            self.enemies.append(enemy)
            
    def update(self, dt):
        if self.game_over or self.victory:
            return
            
        # Обновление врагов
        for enemy in self.enemies[:]:
            enemy.update(dt)
            # Проверка достижения левого края
            if enemy.x < 50:
                self.player.take_damage(enemy.word_length)
                self.enemies.remove(enemy)
                
        # Проверка здоровья игрока
        if self.player.health <= 0:
            self.game_over = True
            
        # Проверка уровня
        if self.player.exp >= self.player.exp_to_next:
            self.level_up()
            
        # Спавн врагов
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            self.spawn_delay = max(0.5, 2.0 - self.level * 0.2)
            
        # Обновление клавиатуры
        self.keyboard.update(dt)
        
    def level_up(self):
        """Повышение уровня"""
        self.level += 1
        self.player.level_up()
        self.spawn_delay = max(0.5, 2.0 - self.level * 0.2)
        
    def draw(self):
        """Отрисовка игры"""
        self.screen.fill(self.colors['background'])
        
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
        else:
            self.draw_game()
            
    def draw_game(self):
        """Отрисовка игрового процесса"""
        # Верхняя панель
        self.draw_ui()
        
        # Игрок
        self.player.draw(self.screen, self.main_font)
        
        # Враги
        for enemy in self.enemies:
            enemy.draw(self.screen, self.main_font)
            # Подсветка если слово совпадает с вводимым
            if enemy.word == self.typed_word:
                pygame.draw.rect(self.screen, self.colors['enemy_hover'], 
                               (enemy.x - 5, enemy.y - 25, 
                                enemy.width + 10, enemy.height + 10), 2)
                
        # Виртуальная клавиатура
        self.keyboard.draw(self.screen)
        
        # Поле ввода
        self.draw_input_field()
        
    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Здоровье
        health_text = f"❤️ {self.player.health}"
        health_surface = self.main_font.render(health_text, True, self.colors['health'])
        self.screen.blit(health_surface, (20, 20))
        
        # Опыт
        exp_text = f"✨ {self.player.exp}/{self.player.exp_to_next}"
        exp_surface = self.main_font.render(exp_text, True, self.colors['exp'])
        self.screen.blit(exp_surface, (20, 60))
        
        # Счет
        score_text = f"🎯 {self.score}"
        score_surface = self.main_font.render(score_text, True, self.colors['text'])
        self.screen.blit(score_surface, (20, 100))
        
        # Уровень
        level_text = f"📊 Уровень {self.level}"
        level_surface = self.main_font.render(level_text, True, self.colors['text'])
        self.screen.blit(level_surface, (self.width - 200, 20))
        
    def draw_input_field(self):
        """Отрисовка поля ввода"""
        # Поле ввода
        input_rect = pygame.Rect(50, self.height - 50, 400, 40)
        pygame.draw.rect(self.screen, self.colors['ui'], input_rect)
        pygame.draw.rect(self.screen, self.colors['text'], input_rect, 2)
        
        # Текст ввода
        input_text = self.typed_word + "█" if pygame.time.get_ticks() % 1000 < 500 else self.typed_word
        text_surface = self.main_font.render(input_text, True, self.colors['text'])
        self.screen.blit(text_surface, (60, self.height - 42))
        
    def draw_game_over(self):
        """Отрисовка экрана проигрыша"""
        # Затемнение
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Текст
        game_over_text = self.title_font.render("ИГРА ОКОНЧЕНА", True, (255, 100, 100))
        score_text = self.main_font.render(f"Счет: {self.score}", True, self.colors['text'])
        restart_text = self.small_font.render("Нажмите R для рестарта", True, self.colors['text'])
        
        text_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 50))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
        
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        
    def draw_victory(self):
        """Отрисовка экрана победы"""
        victory_text = self.title_font.render("ПОБЕДА!", True, (100, 255, 100))
        score_text = self.main_font.render(f"Счет: {self.score}", True, self.colors['text'])
        restart_text = self.small_font.render("Нажмите R для новой игры", True, self.colors['text'])
        
        text_rect = victory_text.get_rect(center=(self.width//2, self.height//2 - 50))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
        
        self.screen.blit(victory_text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        
    def reset_game(self):
        """Сброс игры"""
        self.player = Player(50, self.height // 2)
        self.enemies = []
        self.score = 0
        self.level = 1
        self.typed_word = ""
        self.game_over = False
        self.victory = False
        self.enemy_spawn_timer = 0
        self.spawn_delay = 2.0