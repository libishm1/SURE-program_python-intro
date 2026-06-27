#aftr drawing the hexagon, let's fill it with rotated hexagons like a spirograpgh filled with colours
import turtle
import random

# Setup the screen and turtle
screen = turtle.Screen()
screen.bgcolor("black")

t = turtle.Turtle()
t.speed(0)  # Set speed to fastest
t.hideturtle()  # Hide the turtle arrow for a cleaner look

colors = ["white", "orange", "yellow", "green", "blue", "purple", "cyan", "magenta", "lime", "pink"]

def draw_hexagon(size, color):
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(6):
        t.forward(size)
        t.right(60)
    t.end_fill()

# Draw a spiral of scaled and rotated hexagons
for i in range(100):
    color = random.choice(colors)
    draw_hexagon(150 - i * 1.2, color)
    t.forward(i * 0.5)
    t.right(10)


turtle.done()
