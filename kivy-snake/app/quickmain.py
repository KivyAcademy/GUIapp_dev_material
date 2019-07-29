from kivy.app import App
from kivy.core.window import Window
from kivy import properties as kp
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import sp
from kivy.animation import Animation

from random import randint

from collections import defaultdict


DOWN = 'down'
UP = 'up'
LEFT = 'left'
RIGHT = 'right'


FLOOR = 'floor'
SNAKE = 'snake'
FRUIT = 'fruit'


_direction_group = {LEFT: 'horizontal',
                    UP: 'vertical',
                    RIGHT: 'horizontal',
                    DOWN: 'vertical'}


_keycode_directions = {276: LEFT,
                       273: UP,
                       275: RIGHT,
                       274: DOWN}


_direction_values = {LEFT: (-1, 0),
                     UP: (0, 1),
                     RIGHT: (1, 0),
                     DOWN: (0, -1)}


SQUARE_SIZE = sp(20)
MOVESPEED = .1
STARTING_LENGHT = 4
COLS = int(Window.width / SQUARE_SIZE)
ROWS = int(Window.height / SQUARE_SIZE)


class Square(Widget):
    bgcolor = kp.ListProperty([0,0,0,0])
    coord = kp.ListProperty([0, 0])


class FruitSquare(Square):
    pass


class SnakeApp(App):
    direction = kp.StringProperty(RIGHT, options=[LEFT, UP, RIGHT, DOWN])

    block_input = kp.BooleanProperty()

    snake = kp.ListProperty()
    head = kp.ListProperty()
    lenght = kp.NumericProperty(STARTING_LENGHT)

    square_size = kp.NumericProperty(SQUARE_SIZE)
    alpha = kp.NumericProperty(0)

    fruit = kp.ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_handler)
        Window.bind(on_touch_move=self.touch_handler)
        self.snake_squares = defaultdict(lambda: Square())
        self.buffer_direction = None
        self.fruit = self.new_food_coord

    def die(self, name):
        self.lenght = STARTING_LENGHT
        self.head = self.new_head_coord
        self.snake.clear()
        self.root.clear_widgets()
        self.root.add_widget(FruitSquare())
        self.play_dead_animation()

    def play_dead_animation(self):
        self.alpha = .5
        Animation(alpha=0, duration=.15).start(self)

    def got_fruit(self):
        self.lenght += 1
        self.fruit = self.new_food_coord

    def on_direction(self, *args):
        self.block_input = True

    @property
    def new_food_coord(self):
        while True:
            new_coord = [randint(0, max_ -1) for max_ in (COLS, ROWS)]
            if new_coord not in self.snake:
                return new_coord
    @property
    def new_head_coord(self):
        return [randint(2, max_ - 2) for max_ in (COLS, ROWS)]

    def on_start(self):
        Clock.schedule_interval(self.move, MOVESPEED)
        self.head = self.new_head_coord
        self.root.add_widget(FruitSquare())

    def on_head(self, *args):
        if self.head == self.fruit:
            self.got_fruit()
        if self.head in self.snake:
            self.die('yourself')
        self.snake = self.snake[-self.lenght:] + [self.head]

    def move(self, *args):
        new_head = [sum(x) for x in zip(self.head, _direction_values[self.direction])]
        if not self.check_in_bounds(new_head):
            return self.die('wall')
        self.head = new_head
        self.block_input = False
        if self.buffer_direction:
            self.change_direction(self.buffer_direction)

    def on_snake(self, *args):
        for index, coord in enumerate(self.snake):
            square = self.snake_squares[index]
            square.coord = coord
            if not square.parent:
                self.root.add_widget(square)

    def check_in_bounds(self, pos):
        return all(0 <= pos[x] <= (dim - 1) for x, dim in enumerate([COLS, ROWS]))

    def key_handler(self, __, keycode, *_):
        try:
            self.try_change_direction(_keycode_directions[keycode])
        except KeyError:
            pass

    def touch_handler(self, _, touch):
        vert = touch.dsy
        horz = touch.dsx
        if any(abs(direction) > .03 for direction in (vert, horz)):
            if abs(horz) > abs(vert):
                new_direction = RIGHT if horz > 0 else LEFT
            else:
                new_direction = UP if vert > 0 else DOWN
            self.try_change_direction(new_direction)

    def try_change_direction(self, new_direction):
        if self.block_input:
            self.buffer_direction = new_direction
        else:
            self.buffer_direction = None
            self.change_direction(new_direction)
        self.block_input = True

    def change_direction(self, new_direction):
        if _direction_group[self.direction] != _direction_group[new_direction]:
            self.direction = new_direction


if __name__ == '__main__':
    SnakeApp().run()
