import turtle
from my_turtle import drawSquare
from app_data import startPoint, endPoint
from mc import mc
sc = turtle.Screen()
pen = turtle.Turtle()

root_x = -400
root_z = -400

drawSquare(pen, root_x, root_z, endPoint['x'] - startPoint['x'], endPoint['z'] - startPoint['z'])
listpl = []
for pl in mc.getPlayerEntityIds():
    listpl.append(turtle)
sc.mainloop()
