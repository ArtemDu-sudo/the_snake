from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс, от которого наследуются игровые объекты."""
    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        """Инициализирует позицию и цвет объекта"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на поле. Переопределяется в потомках"""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и и как оно работает"""
    def __init__(self):
        """Задаёт цвет яблока"""
        super().__init__((320, 240), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        x = randint(0, int(GRID_WIDTH) - 1) * GRID_SIZE
        y = randint(0, int(GRID_HEIGHT) - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        pygame.draw.rect(screen, self.body_color,
                         (*self.position, GRID_SIZE, GRID_SIZE))


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение"""
    def __init__(self):
        """Инициализирует начальное состояние змейки"""
        self.positions = [(320, 240)]
        self.length = len(self.positions)
        super().__init__(self.positions[0], SNAKE_COLOR)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки (включает добавление новый головы и
        удаление хвоста)"""
        head = self.get_head_position()
        new_x = head[0] + self.direction[0] * GRID_SIZE
        new_y = head[1] + self.direction[1] * GRID_SIZE
        new_x = new_x % SCREEN_WIDTH
        new_y = new_y % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, убирая за ней след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, меняя направление движения змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
