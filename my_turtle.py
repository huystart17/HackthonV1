def drawSquare(pen, x1, y1, x2, y2):
    pen.penup()
    pen.setpos(x1, y1)
    pen.pendown()
    pen.setpos(x2, y1)
    pen.setpos(x2, y2)
    pen.setpos(x1, y2)
    pen.setpos(x1, y1)


