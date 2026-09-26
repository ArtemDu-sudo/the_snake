import sys
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Начальная позиция игровых объектов - центр игрового поля:
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона, границы ячейки, яблока и змейки:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются игровые объекты"""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализирует позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на поле, переопределяется в потомках"""
        raise NotImplementedError(
            f'Метод draw не переопределён в классе {type(self).__name__}.'
        )

    def draw_cell(self, position, color=None):
        """Отрисовывает одну игровую ячейку заданным цветом с рамкой"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и его поведение"""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=None):
        """Задаёт цвет яблока и позицию вне занятых клеток"""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию яблока вне занятых клеток"""
        occupied_positions = occupied_positions or []
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение"""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку, сбрасывая её в начальное состояние"""
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки.

        Добавляет новую голову в начало списка и удаляет хвост,
        если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop(-1)
            if len(self.positions) > self.length
            else None
        )

    def draw(self):
        """Отрисовывает голову змейки и стирает след хвоста"""
        self.draw_cell(self.get_head_position())

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.position = CENTER_POSITION
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, меняя направление движения змейки"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN and event.key in TURNS:
            new_direction, opposite_direction = TURNS[event.key]
            if game_object.direction != opposite_direction:
                game_object.next_direction = new_direction


def main():
    """Запускает основной игровой цикл"""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
