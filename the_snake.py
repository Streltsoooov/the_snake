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
            GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE
        )
        self.body_color = None

    def draw(self):
        """
        Метод для отрисовки объекта на поле.
        Переопределен в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс для яблока
    Включает в себя опредление случайной позиции появления яблока
    и его отрисовку на игровом поле
    """

    def __init__(self):
        """Инициализация Apple"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Определение позиции для Apple"""
        coordinates_on_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        coordinates_on_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return coordinates_on_x, coordinates_on_y

    def draw(self):
        """Отрисовка Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки
    Включает в себя метод изменения направления, обычное перемещение,
    отрисовку фигуры на поле, определение координат головы
    и сброс змейки в исходное состояние
    """

    def __init__(self):
        """Инициализация Snake"""
        super().__init__()
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = UP
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление после нажатия на кнопку"""
        handle_keys(self)
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, двигая голову"""
        coordinates_x_direction, coordinates_y_direction = self.direction
        coordinates_on_x, coordinates_on_y = self.positions[0]
        new_position = (
            coordinates_on_x + coordinates_x_direction * GRID_SIZE,
            coordinates_on_y + coordinates_y_direction * GRID_SIZE
        )
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

        #  Переопредление списка в случае выхода за границы
        self.positions = [
            (coordinates_x % SCREEN_WIDTH, coordinates_y % SCREEN_HEIGHT)
            for coordinates_x, coordinates_y in self.positions
        ]

    def draw(self):
        """Метод для отрисовки змейки"""
        #  Отрисовка змейки с послденим сегментом
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        #  Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        for pos in self.positions:
            snake_rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, snake_rect)
        self.positions = [self.position]
        self.length = 1


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    """Тело игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()
        #  Проверка на врезание
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        #  Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()
