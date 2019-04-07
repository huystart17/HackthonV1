from turtle import *
from turtle_tool import *
from City import *

pen = Turtle()
pen.speed(0)
draw_square_fill_two_point(pen, 650, 650, 950, 950, '', 'black')
pen.color('blue')

draw_square_two_point(pen, 869, 650, 789, 950)
pen.color('white')

pen.down()
pen.sety(-300)
pen.sety(300)

z_root = 650
width = 81
space = 29
for i in range(3):
    draw_square_fill_two_point(pen, 870,z_root , 950,z_root + width ,'', 'brown')
    z_root  =z_root + width  + space

ct.load('air_port', '2')
ct.monitor()
# ct.clear()
# ct.clear()

