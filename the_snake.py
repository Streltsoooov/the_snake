from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
HALF_GRID_WIDTH = GRID_WIDTH // 2
HALF_GRID_HEIGHT = GRID_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTION = [UP, DOWN, LEFT, RIGHT]

# Словарь изменения направления
# Нажатая клавиша, старое направление -> Новое направление
TURNS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для объектов"""

    def __init__(self):
        """Метод для инициализации конкретного объекта"""
        self.position = (
            HALF_GRID_WIDTH * GRID_SIZE, HALF_GRID_HEIGHT * GRID_SIZE
        )
        self.body_color = None

    def draw(self):
        """
        Метод для отрисовки объекта на поле.
        Переопределен в дочерних классах
        """

    def draw_cell(self, position, color, bord_color=(0, 0, 0)):
        """Метод отрисовки 1 ячейки"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, bord_color, rect, 1)


class Apple(GameObject):
    """Класс для яблока
    Включает в себя опредление случайной позиции появления яблока
    и его отрисовку на игровом поле
    """

    def __init__(self, position_snake=(
            HALF_GRID_WIDTH * GRID_SIZE, HALF_GRID_HEIGHT * GRID_SIZE)):
        """Инициализация Apple"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(position_snake)

    def randomize_position(self, snake_current_position):
        """Определение позиции для Apple"""
        while True:
            new_coordinates = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_coordinates not in snake_current_position:
                return new_coordinates

    def draw(self):
        """Отрисовка Apple"""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Класс для змейки
    Включает в себя метод изменения направления, обычное перемещение,
    отрисовку фигуры на поле, определение координат головы
    и сброс змейки в исходное состояние
    """

    def __init__(self):
        """Инициализация Snake"""
        super().__init__()
        self.reset()

    def update_direction(self, new_direction):
        """Обновляет направление после нажатия на кнопку"""
        self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки, двигая голову"""
        coordinates_x_direction, coordinates_y_direction = self.direction
        coordinates_on_x, coordinates_on_y = self.get_head_position()
        new_position = (
            coordinates_on_x + coordinates_x_direction * GRID_SIZE,
            coordinates_on_y + coordinates_y_direction * GRID_SIZE
        )
        self.positions.insert(0, new_position)
        self.positions = [
            (coordinates_x % SCREEN_WIDTH, coordinates_y % SCREEN_HEIGHT)
            for coordinates_x, coordinates_y in self.positions
        ]

        self.last = self.positions.pop() \
            if len(self.positions) > self.length else None

    def draw(self):
        """Метод для отрисовки змейки"""
        #  Отрисовка змейки с послденим сегментом
        self.draw_cell(self.get_head_position(), SNAKE_COLOR, BORDER_COLOR)

        #  Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.last = None
        self.length = 1
        self.direction = choice(DIRECTION)
        screen.fill((BOARD_BACKGROUND_COLOR))


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            game_object.update_direction(TURNS.get(
                (event.key, game_object.direction),
                game_object.direction
            ))


def main():
    """Тело игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.position)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        #  Проверка на врезание
        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()
            apple.draw_cell(apple.position, BOARD_BACKGROUND_COLOR)
            apple.position = apple.randomize_position(snake.positions)
        #  Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
