from app_data import *


def draw_square(pen, x, y, width):
    pass


def draw_rect(pen, x, y, w, l):
    pen.penup()
    pen.setpos(x, y)
    pen.pendown()
    pen.setpos(x + w, y)
    pen.setpos(x + w, y + l)
    pen.setpos(x, y + l)
    pen.setpos(x, y)
    pen.penup()
    pass


def draw_square_two_point(pen, x1, y1, x2, y2, text=""):
    pen.penup()
    _x1 = x1 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y1 = y1 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    _x2 = x2 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y2 = y2 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    print("_x1 = {} , _x2 = {}, _y1 = {} , _y2 = {}".format(_x1, _x2, _y1, _y2))
    print("x1 = {} , x2 = {}, y1 = {} , y2 = {}".format(x1, x2, y1, y2))
    print("text= ", text)
    _x1 = _x1 * turtle_ratio
    _x2 = _x2 * turtle_ratio
    _y1 = _y1 * turtle_ratio
    _y2 = _y2 * turtle_ratio

    print("======")
    pen.setpos(_x1, _y1)
    pen.pendown()
    pen.setpos(_x1, _y2)
    pen.setpos(_x2, _y2)
    pen.setpos(_x2, _y1)
    pen.setpos(_x1, _y1)
    pen.penup()
    pen.setpos((_x1 + _x2) / 2, (_y1 + _y2) / 2)
    pen.write(text, align='center')
    pen.ht()
    pass

def draw_square_fill_two_point(pen, x1, y1, x2, y2, text="" ,fill_color= 'yellow'):
    pen.penup()
    _x1 = x1 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y1 = y1 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    _x2 = x2 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y2 = y2 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    print("_x1 = {} , _x2 = {}, _y1 = {} , _y2 = {}".format(_x1, _x2, _y1, _y2))
    print("x1 = {} , x2 = {}, y1 = {} , y2 = {}".format(x1, x2, y1, y2))
    print("text= ", text)
    _x1 = _x1 * turtle_ratio
    _x2 = _x2 * turtle_ratio
    _y1 = _y1 * turtle_ratio
    _y2 = _y2 * turtle_ratio

    print("======")
    pen.setpos(_x1, _y1)
    pen.pendown()
    pen.begin_fill()
    pen.fillcolor(fill_color)
    pen.setpos(_x1, _y2)
    pen.setpos(_x2, _y2)
    pen.setpos(_x2, _y1)
    pen.setpos(_x1, _y1)
    pen.end_fill()
    pen.penup()
    pen.setpos((_x1 + _x2) / 2, (_y1 + _y2) / 2)
    pen.write(text, align='center')
    pen.ht()
    pass


def is_in_region(x, y, x1, y1, x2, y2):
    _x1 = x1 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y1 = y1 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    _x2 = x2 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y2 = y2 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    _x1 = _x1 * turtle_ratio
    _x2 = _x2 * turtle_ratio
    _y1 = _y1 * turtle_ratio
    _y2 = _y2 * turtle_ratio
    in_x = _x1 >= x >= _x2 or _x1 <= x <= _x2
    in_y = _y1 >= y >= _y2 or _y1 <= y <= _y2
    return in_x and in_y


def move_player(pen, x1, y1, text=""):
    _x1 = x1 - startPoint['x'] - abs((startPoint['x'] - endPoint['x'])) / 2
    _y1 = y1 - startPoint['z'] - abs((startPoint['z'] - endPoint['z'])) / 2
    _x1 = _x1 * turtle_ratio
    _y1 = _y1 * turtle_ratio
    pen.clear()
    pen.setpos(_x1, _y1)
    pen.write(text)
