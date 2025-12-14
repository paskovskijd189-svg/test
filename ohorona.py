import pygame
import random
import sys
from datetime import datetime, timedelta

# Инициализация pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE = (70, 130, 200)
YELLOW = (255, 220, 0)
LIGHT_GRAY = (200, 200, 200)
BEIGE = (245, 222, 179)

# Имена для генерации
FIRST_NAMES = ["Иван", "Мария", "Петр", "Анна", "Дмитрий", "Елена", "Сергей", "Ольга", "Александр", "Наталья"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Козлов", "Смирнов", "Попов", "Волков", "Соколов", "Лебедев", "Морозов"]
PATRONYMICS = ["Иванович", "Петрович", "Сергеевич", "Александрович", "Дмитриевич", "Михайлович", "Андреевич", "Николаевич"]
PATRONYMICS_F = ["Ивановна", "Петровна", "Сергеевна", "Александровна", "Дмитриевна", "Михайловна", "Андреевна", "Николаевна"]
GROUPS = ["ИВТ-401", "ПМИ-302", "КБ-201", "ИБ-403", "ПИ-304", "ФИИТ-202"]


class Button:
    """Класс кнопки"""
    def __init__(self, x, y, width, height, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
        
    def draw(self, screen, font):
        color = tuple(min(c + 30, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)


class Document:
    """Класс студенческого билета"""
    def __init__(self, person, day, create_error=False):
        self.person = person
        self.name = person.name
        self.last_name = person.last_name
        self.patronymic = person.patronymic
        self.number = f"{random.randint(100000, 999999)}"
        self.group = random.choice(GROUPS)
        
        # Даты
        issue_date = datetime.now() - timedelta(days=random.randint(0, 730))
        self.issue_date = issue_date.strftime("%d.%m.%Y")
        valid_until = issue_date + timedelta(days=1095)  # 3 года
        self.valid_until = valid_until.strftime("%d.%m.%Y")
        
        # Ошибки в документе
        self.has_error = False
        self.error_type = None
        
        if create_error:
            error_chance = min(0.3 + day * 0.05, 0.7)
            if random.random() < error_chance:
                self.has_error = True
                self.create_error(valid_until)
    
    def create_error(self, valid_until):
        """Создать ошибку в документе"""
        error_types = ["expired", "wrong_name", "wrong_photo", "fake_number"]
        self.error_type = random.choice(error_types)
        
        if self.error_type == "expired":
            old_date = datetime.now() - timedelta(days=random.randint(30, 365))
            self.valid_until = old_date.strftime("%d.%m.%Y")
        elif self.error_type == "wrong_name":
            if random.random() < 0.5:
                self.name = random.choice(FIRST_NAMES)
            else:
                self.last_name = random.choice(LAST_NAMES)
        elif self.error_type == "fake_number":
            self.number = f"{random.randint(1, 9)}" * 6
    
    def draw(self, screen, x, y):
        """Отрисовка студенческого билета"""
        doc_width = 400
        doc_height = 300
        
        # Фон документа
        pygame.draw.rect(screen, BEIGE, (x, y, doc_width, doc_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (x, y, doc_width, doc_height), 3, border_radius=10)
        
        # Заголовок
        title_font = pygame.font.Font(None, 28)
        title = title_font.render("СТУДЕНЧЕСКИЙ БИЛЕТ", True, BLACK)
        screen.blit(title, (x + 90, y + 15))
        
        # Фото (упрощённый портрет)
        photo_x = x + 20
        photo_y = y + 50
        self.person.draw_portrait(screen, photo_x, photo_y, 80)
        
        # Информация
        info_x = x + 120
        info_y = y + 60
        font = pygame.font.Font(None, 24)
        
        info_lines = [
            f"Фамилия: {self.last_name}",
            f"Имя: {self.name}",
            f"Отчество: {self.patronymic}",
            f"№: {self.number}",
            f"Группа: {self.group}",
            f"Выдан: {self.issue_date}",
            f"Действителен до: {self.valid_until}"
        ]
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, BLACK)
            screen.blit(text, (info_x, info_y + i * 30))
    
    @staticmethod
    def draw_reference(screen, x, y):
        """Отрисовка эталонного студенческого билета"""
        doc_width = 400
        doc_height = 300
        
        # Фон документа с зелёной рамкой (эталон)
        pygame.draw.rect(screen, BEIGE, (x, y, doc_width, doc_height), border_radius=10)
        pygame.draw.rect(screen, GREEN, (x, y, doc_width, doc_height), 3, border_radius=10)
        
        # Заголовок
        title_font = pygame.font.Font(None, 28)
        title = title_font.render("ОБРАЗЕЦ БИЛЕТА", True, GREEN)
        screen.blit(title, (x + 110, y + 15))
        
        # Пример портрета
        photo_x = x + 20
        photo_y = y + 50
        pygame.draw.rect(screen, LIGHT_GRAY, (photo_x, photo_y, 80, 80), border_radius=5)
        pygame.draw.rect(screen, BLACK, (photo_x, photo_y, 80, 80), 2, border_radius=5)
        
        # Простой портрет-пример
        pygame.draw.circle(screen, BEIGE, (photo_x + 40, photo_y + 30), 20)
        pygame.draw.rect(screen, BLUE, (photo_x + 20, photo_y + 50, 40, 25))
        
        # Информация с примерами
        info_x = x + 120
        info_y = y + 60
        font = pygame.font.Font(None, 24)
        
        info_lines = [
            "Фамилия: ИВАНОВ",
            "Имя: ИВАН",
            "Отчество: ИВАНОВИЧ",
            "№: 123456 (6 цифр)",
            "Группа: ИВТ-401",
            "Выдан: ДД.ММ.ГГГГ",
            "Действителен до: ДД.ММ.ГГГГ"
        ]
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, BLACK)
            screen.blit(text, (info_x, info_y + i * 30))
        
        # Пояснения
        notes_y = y + 240
        notes_font = pygame.font.Font(None, 20)
        notes = [
            "• Фото должно совпадать с человеком",
            "• Срок действия не должен быть просрочен",
            "• Номер должен содержать разные цифры"
        ]
        
        for i, note in enumerate(notes):
            text = notes_font.render(note, True, DARK_GRAY)
            screen.blit(text, (x + 10, notes_y + i * 20))


class MetalDetector:
    """Класс металлодетектора"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 200
        self.alarm = False
        self.alarm_timer = 0
        
    def check(self, person):
        """Проверка персонажа"""
        if person.has_contraband:
            self.alarm = True
            self.alarm_timer = 60
            
    def update(self):
        """Обновление таймера сигнала"""
        if self.alarm_timer > 0:
            self.alarm_timer -= 1
            if self.alarm_timer == 0:
                self.alarm = False
    
    def draw(self, screen):
        """Отрисовка металлодетектора"""
        # Стойки
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, 20, self.height))
        pygame.draw.rect(screen, DARK_GRAY, (self.x + self.width - 20, self.y, 20, self.height))
        
        # Верхняя перекладина
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, self.width, 30))
        
        # Индикатор
        color = RED if self.alarm else GREEN
        pygame.draw.circle(screen, color, (self.x + self.width // 2, self.y + 15), 8)


class Gate:
    """Класс калитки/турникета"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 100
        self.open = False
        
    def draw(self, screen):
        """Отрисовка калитки"""
        # Стойки
        pygame.draw.rect(screen, DARK_GRAY, (self.x - 30, self.y, 25, self.height))
        pygame.draw.rect(screen, DARK_GRAY, (self.x + self.width + 5, self.y, 25, self.height))
        
        # Барьер
        if not self.open:
            pygame.draw.rect(screen, RED, (self.x, self.y + 40, self.width, 8))


class Person:
    """Класс персонажа"""
    def __init__(self, day):
        self.x = -100
        self.y = 150
        self.width = 40
        self.height = 80
        self.speed = 2
        
        # Внешность
        self.gender = random.choice(["M", "F"])
        self.name = random.choice(FIRST_NAMES)
        self.last_name = random.choice(LAST_NAMES)
        self.patronymic = random.choice(PATRONYMICS if self.gender == "M" else PATRONYMICS_F)
        
        # Визуальные характеристики
        self.head_color = random.choice([BEIGE, (220, 180, 140), (180, 140, 100)])
        self.hair_color = random.choice([BLACK, (101, 67, 33), (193, 154, 107), YELLOW])
        self.clothes_color = random.choice([BLUE, RED, GREEN, DARK_GRAY, (139, 69, 19)])
        self.hair_style = random.choice(["short", "long", "bald"])
        
        # Контрабанда
        contraband_chance = min(0.2 + day * 0.03, 0.5)
        self.has_contraband = random.random() < contraband_chance
        
        # Состояние
        self.state = "walking_to_detector"
        self.target_x = 550
        self.document = None
        
    def create_document(self, day):
        """Создать документ для персонажа"""
        self.document = Document(self, day, create_error=True)
    
    def update(self, metal_detector, gate):
        """Обновление позиции персонажа"""
        if self.state == "walking_to_detector":
            self.x += self.speed
            if self.x >= self.target_x:
                self.state = "passing_detector"
                metal_detector.check(self)
                
        elif self.state == "passing_detector":
            self.x += self.speed
            if self.x >= self.target_x + 150:
                self.state = "walking_to_gate"
                self.y = 150
                self.target_x = SCREEN_WIDTH // 2 - 50
                
        elif self.state == "walking_to_gate":
            if self.y < 500:
                self.y += self.speed
            else:
                self.x += self.speed * 0.5
                if self.x >= self.target_x:
                    self.state = "at_gate"
                    
        elif self.state == "leaving":
            if gate.open:
                self.y += self.speed
            else:
                self.x -= self.speed
                
    def draw(self, screen):
        """Отрисовка персонажа"""
        # Тело
        pygame.draw.rect(screen, self.clothes_color, 
                        (self.x, self.y + 30, self.width, self.height - 30))
        
        # Голова
        pygame.draw.circle(screen, self.head_color, 
                          (int(self.x + self.width // 2), int(self.y + 15)), 15)
        
        # Волосы
        if self.hair_style == "short":
            pygame.draw.circle(screen, self.hair_color,
                             (int(self.x + self.width // 2), int(self.y + 10)), 16, 4)
        elif self.hair_style == "long":
            pygame.draw.rect(screen, self.hair_color,
                           (self.x + 8, self.y + 5, 24, 25))
            
    def draw_portrait(self, screen, x, y, size):
        """Отрисовка портрета для документа"""
        # Голова
        pygame.draw.circle(screen, self.head_color, (x + size // 2, y + size // 3), size // 3)
        
        # Волосы
        if self.hair_style == "short":
            pygame.draw.circle(screen, self.hair_color, (x + size // 2, y + size // 4), size // 3, 3)
        elif self.hair_style == "long":
            pygame.draw.rect(screen, self.hair_color, (x + size // 6, y + 5, size * 2 // 3, size // 2))
            
        # Тело
        pygame.draw.rect(screen, self.clothes_color, (x + size // 4, y + size // 2, size // 2, size // 2))


class Game:
    """Главный класс игры"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Papers, Please: Campus Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Шрифты
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        
        # Игровые объекты
        self.metal_detector = MetalDetector(550, 100)
        self.gate = Gate(SCREEN_WIDTH // 2 - 30, 520)
        
        # Кнопки
        self.accept_button = Button(800, 650, 150, 50, "Пропустить", GREEN)
        self.deny_button = Button(970, 650, 150, 50, "Отказать", RED)
        self.show_reference_button = Button(480, 650, 200, 50, "Показать образец", BLUE)
        
        # Игровое состояние
        self.day = 1
        self.correct = 0
        self.mistakes = 0
        self.current_person = None
        self.showing_document = False
        self.people_processed = 0
        self.people_per_day = 5
        self.reference_document_visible = False
        
        # Текущая дата и время в игре
        self.current_date = datetime.now()
        
        self.spawn_new_person()
        
    def spawn_new_person(self):
        """Создать нового персонажа"""
        if self.people_processed < self.people_per_day:
            self.current_person = Person(self.day)
            self.current_person.create_document(self.day)
            self.showing_document = False
            self.reference_document_visible = False
        else:
            self.next_day()
            
    def next_day(self):
        """Переход к следующему дню"""
        self.day += 1
        self.current_date += timedelta(days=1)
        self.people_processed = 0
        self.people_per_day = min(5 + self.day, 10)
        self.spawn_new_person()
        
    def check_decision(self, allow):
        """Проверка решения игрока"""
        doc = self.current_person.document
        person = self.current_person
        
        # Правильное решение: отказать если есть ошибка в документе ИЛИ контрабанда
        should_deny = doc.has_error or person.has_contraband
        
        if allow:
            if should_deny:
                self.mistakes += 1
            else:
                self.correct += 1
            self.gate.open = True
        else:
            if should_deny:
                self.correct += 1
            else:
                self.mistakes += 1
            self.gate.open = False
            
        self.current_person.state = "leaving"
        self.people_processed += 1
        
    def handle_events(self):
        """Обработка событий"""
        mouse_pos = pygame.mouse.get_pos()
        self.accept_button.update_hover(mouse_pos)
        self.deny_button.update_hover(mouse_pos)
        self.show_reference_button.update_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.showing_document:
                    if self.accept_button.is_clicked(mouse_pos):
                        self.check_decision(True)
                        self.reference_document_visible = False
                    elif self.deny_button.is_clicked(mouse_pos):
                        self.check_decision(False)
                        self.reference_document_visible = False
                    elif self.show_reference_button.is_clicked(mouse_pos):
                        self.reference_document_visible = not self.reference_document_visible
                        
    def update(self):
        """Обновление игровой логики"""
        if self.current_person:
            self.current_person.update(self.metal_detector, self.gate)
            
            if self.current_person.state == "at_gate":
                self.showing_document = True
                
            if self.current_person.state == "leaving":
                if self.current_person.y > SCREEN_HEIGHT or self.current_person.x < -100:
                    self.spawn_new_person()
                    
        self.metal_detector.update()
        
    def draw(self):
        """Отрисовка всех элементов"""
        self.screen.fill(LIGHT_GRAY)
        
        # Разделительная линия
        pygame.draw.line(self.screen, BLACK, (0, 400), (SCREEN_WIDTH, 400), 3)
        
        # Металлодетектор
        self.metal_detector.draw(self.screen)
        
        # Калитка
        self.gate.draw(self.screen)
        
        # Персонаж
        if self.current_person:
            self.current_person.draw(self.screen)
            
        # Интерфейс проверки (когда персонаж у калитки)
        if self.showing_document and self.current_person:
            # Вертикальная разделительная линия по центру нижней части
            pygame.draw.line(self.screen, BLACK, (SCREEN_WIDTH // 2, 400), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 3)
            
            # ЛЕВАЯ ЧАСТЬ - Студенческий билет
            if not self.reference_document_visible:
                self.current_person.document.draw(self.screen, 50, 450)
            else:
                Document.draw_reference(self.screen, 50, 450)
            
            # ПРАВАЯ ЧАСТЬ - Живой персонаж крупным планом
            person_display_x = SCREEN_WIDTH // 2 + 150
            person_display_y = 500
            
            # Голова
            pygame.draw.circle(self.screen, self.current_person.head_color, 
                             (person_display_x, person_display_y), 45)
            
            # Волосы
            if self.current_person.hair_style == "short":
                pygame.draw.circle(self.screen, self.current_person.hair_color,
                                 (person_display_x, person_display_y - 10), 48, 8)
            elif self.current_person.hair_style == "long":
                pygame.draw.rect(self.screen, self.current_person.hair_color,
                               (person_display_x - 36, person_display_y - 30, 72, 60))
            
            # Тело
            pygame.draw.rect(self.screen, self.current_person.clothes_color,
                           (person_display_x - 40, person_display_y + 40, 80, 120))
            
            # Рамка вокруг персонажа
            pygame.draw.rect(self.screen, BLACK, 
                           (person_display_x - 80, person_display_y - 80, 160, 260), 3)
            
            # Кнопки управления внизу
            self.show_reference_button.draw(self.screen, self.font)
            self.accept_button.draw(self.screen, self.font)
            self.deny_button.draw(self.screen, self.font)
            
        # Статистика
        day_text = self.font.render(f"День: {self.day}", True, BLACK)
        correct_text = self.font.render(f"Правильно: {self.correct}", True, GREEN)
        mistakes_text = self.font.render(f"Ошибок: {self.mistakes}", True, RED)
        people_text = self.font.render(f"Проверено: {self.people_processed}/{self.people_per_day}", True, BLACK)
        
        self.screen.blit(day_text, (10, 10))
        self.screen.blit(correct_text, (10, 40))
        self.screen.blit(mistakes_text, (10, 70))
        self.screen.blit(people_text, (10, 100))
        
        # Дата и время в правом верхнем углу
        date_str = self.current_date.strftime("%d.%m.%Y")
        time_str = self.current_date.strftime("%H:%M")
        
        date_text = self.font.render(date_str, True, BLACK)
        time_text = self.font.render(time_str, True, BLACK)
        
        # Рамка для даты и времени
        info_box_x = SCREEN_WIDTH - 180
        info_box_y = 10
        pygame.draw.rect(self.screen, WHITE, (info_box_x, info_box_y, 170, 70), border_radius=5)
        pygame.draw.rect(self.screen, BLACK, (info_box_x, info_box_y, 170, 70), 2, border_radius=5)
        
        self.screen.blit(date_text, (info_box_x + 10, info_box_y + 10))
        self.screen.blit(time_text, (info_box_x + 10, info_box_y + 40))
        
        pygame.display.flip()
        
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
