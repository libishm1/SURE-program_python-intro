# ============================================================
# CONCEPT: the list (a data structure that grows and changes)
# ============================================================
# A list holds an ordered sequence of items. We can:
#   append -> add to the end      pop -> remove from the end
#   sort   -> reorder in place
# Each operation MUTATES the list. We redraw the list as a bar
# chart after every step, so the data structure becomes visible.
# Watch how the PICTURE and the PRINTED list always match.
# ============================================================

import time
import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("list as a bar chart: watch it mutate")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()


def draw_bars(data, caption):
    """Redraw the whole list as bars. This is our 'view' of the data."""
    pen.clear()
    pen.penup()
    x0 = -250
    width = 40
    for i, value in enumerate(data):
        x = x0 + i * (width + 6)
        # bar
        pen.goto(x, 0)
        pen.pendown()
        pen.fillcolor("teal")
        pen.begin_fill()
        for dx, dy in [(width, 0), (0, value * 8), (-width, 0), (0, -value * 8)]:
            pen.goto(pen.xcor() + dx, pen.ycor() + dy)
        pen.end_fill()
        pen.penup()
        # value label on top
        pen.goto(x + width / 2, value * 8 + 6)
        pen.color("white")
        pen.write(value, align="center", font=("Arial", 12, "bold"))
        pen.color("black")
    # caption
    pen.goto(0, -40)
    pen.color("yellow")
    pen.write(caption, align="center", font=("Arial", 14, "bold"))
    pen.color("black")
    screen.update()


def step(data, caption):
    print(f"{caption:22s} -> {data}")   # TRACE: list state after each op
    draw_bars(data, caption)
    time.sleep(0.9)                      # pause so students can read it


# ---- the story of one list ------------------------------------
numbers = []
step(numbers, "start: empty list")

for v in [5, 9, 3]:
    numbers.append(v)
    step(numbers, f"append({v})")

removed = numbers.pop()
step(numbers, f"pop() -> {removed}")

numbers.append(7)
numbers.append(1)
step(numbers, "append(7), append(1)")

numbers.sort()
step(numbers, "sort()")

print("\nFinal list:", numbers)
screen.exitonclick()
