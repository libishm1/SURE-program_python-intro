# ============================================================
# CONCEPT: stack vs queue  (two ways to remove items)
# ============================================================
# Same data, different RULE for what comes out next:
#   STACK = LIFO  (Last In, First Out)  -> remove from the END
#   QUEUE = FIFO  (First In, First Out) -> remove from the FRONT
#
# We push the same 5 blocks into both, then remove them one by
# one, so students SEE why the order differs. The order an item
# leaves is the whole point of choosing one structure over the other.
# ============================================================

import time
import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("stack (LIFO) vs queue (FIFO)")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()

COLORS = ["red", "orange", "yellow", "green", "deepskyblue"]


def draw_column(items, x, title):
    """Draw a list as a stack of colored blocks rising from the bottom."""
    pen.penup()
    pen.goto(x, 200)
    pen.color("white")
    pen.write(title, align="center", font=("Arial", 16, "bold"))
    for i, label in enumerate(items):
        y = -150 + i * 44
        pen.goto(x - 50, y)
        pen.pendown()
        pen.fillcolor(COLORS[label % len(COLORS)])
        pen.begin_fill()
        for dx, dy in [(100, 0), (0, 40), (-100, 0), (0, -40)]:
            pen.goto(pen.xcor() + dx, pen.ycor() + dy)
        pen.end_fill()
        pen.penup()
        pen.goto(x, y + 10)
        pen.color("black")
        pen.write(label, align="center", font=("Arial", 14, "bold"))
        pen.color("white")


def render(stack, queue, note):
    pen.clear()
    draw_column(stack, -180, "STACK (LIFO)")
    draw_column(queue,  180, "QUEUE (FIFO)")
    pen.goto(0, -210)
    pen.color("yellow")
    pen.write(note, align="center", font=("Arial", 13, "normal"))
    screen.update()
    time.sleep(1.0)


# ---- push the same items into both ----------------------------
stack, queue = [], []
for item in [1, 2, 3, 4, 5]:
    stack.append(item)
    queue.append(item)
    print(f"push {item} -> stack={stack}  queue={queue}")
render(stack, queue, f"pushed {item} into both")

# ---- now remove everything and watch the order differ --------
while stack or queue:
    s = stack.pop()        # LIFO: take from the END
    q = queue.pop(0)       # FIFO: take from the FRONT
    print(f"stack.pop() -> {s}   |   queue.pop(0) -> {q}")
    render(stack, queue, f"stack removed {s}   |   queue removed {q}")

print("\nStack came out 5,4,3,2,1 (reversed).  Queue came out 1,2,3,4,5 (in order).")
screen.exitonclick()
