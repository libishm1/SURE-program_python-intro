#lets create a Hilbert curve plot with turtle graphics in python make it colourful and interactive
import turtle

def hilbert_curve(t, order, size, angle):
    if order == 0:
        return
    t.left(angle)
    hilbert_curve(t, order - 1, size, -angle)
    t.forward(size)
    t.right(angle)
    hilbert_curve(t, order - 1, size, angle)
    t.forward(size)
    hilbert_curve(t, order - 1, size, angle)
    t.right(angle)
    t.forward(size)
    hilbert_curve(t, order - 1, size, -angle)
    t.left(angle)

# Set up the turtle
screen = turtle.Screen()
t = turtle.Turtle()
t.speed(0)  # Fastest speed
t.pencolor("green")

# Draw the Hilbert curve
hilbert_curve(t, 4, 20, 90)

# Keep the window open
screen.exitonclick()

turtle.done()
turtle.bye()