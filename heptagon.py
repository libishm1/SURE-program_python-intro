#use turtle to draw a heptagon
import turtle
t = turtle.Pen()
#define the color of the heptagon
t.pencolor("blue")
t.fillcolor("red")
t.begin_fill()  
#draw a heptagon
for x in range(7):
    t.forward(100)
    t.left(360/7)#angle of 360/7 degrees to turn the turtle left
    #close the turtle graphics window when clicked
    #fill the heptagon with red color
t.end_fill()
turtle.done()


