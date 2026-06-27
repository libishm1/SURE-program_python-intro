# ============================================================
# CONCEPT: the dictionary  (key -> value lookup)
# ============================================================
# A list finds items by POSITION (numbers[0]).
# A dictionary finds items by a KEY you choose (ages["Sam"]).
# Think of it as labeled boxes: each box has a name (key) on top
# and a value inside. You can add new boxes, change a value, and
# look one up by its key.
#
# We draw each key/value pair as a labeled box and redraw after
# every change, so the data structure stays visible.
# ============================================================

import time
import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("dictionary: key -> value boxes")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()


def draw_dict(d, caption):
    """Redraw every key:value pair as a labeled box."""
    pen.clear()
    pen.penup()
    x0 = -260
    for i, (key, value) in enumerate(d.items()):
        x = x0 + i * 120
        # the box
        pen.goto(x, -40)
        pen.pendown()
        pen.fillcolor("indigo")
        pen.begin_fill()
        for dx, dy in [(100, 0), (0, 80), (-100, 0), (0, -80)]:
            pen.goto(pen.xcor() + dx, pen.ycor() + dy)
        pen.end_fill()
        pen.penup()
        # key label ON TOP of the box
        pen.goto(x + 50, 45)
        pen.color("yellow")
        pen.write(key, align="center", font=("Arial", 14, "bold"))
        # value INSIDE the box
        pen.goto(x + 50, -10)
        pen.color("white")
        pen.write(value, align="center", font=("Arial", 18, "bold"))
    # caption
    pen.goto(0, -120)
    pen.color("orange")
    pen.write(caption, align="center", font=("Arial", 14, "bold"))
    screen.update()
    time.sleep(1.0)


# ---- the story of one dictionary ------------------------------
ages = {}
draw_dict(ages, "start: empty {}")

ages["Sam"] = 20
print("ages['Sam'] = 20 ->", ages)
draw_dict(ages, "add key 'Sam'")

ages["Mia"] = 25
print("ages['Mia'] = 25 ->", ages)
draw_dict(ages, "add key 'Mia'")

ages["Sam"] = 21            # same key -> UPDATES, does not add a new box
print("ages['Sam'] = 21 ->", ages)
draw_dict(ages, "update 'Sam' (same key)")

# look one up by key
who = "Mia"
print(f"\nlook up ages['{who}'] -> {ages[who]}")
draw_dict(ages, f"lookup ages['{who}'] = {ages[who]}")

screen.exitonclick()
