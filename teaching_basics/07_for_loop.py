# ============================================================
# CONCEPT: the for loop + range()
# ============================================================
# A for loop walks through a sequence, one item at a time.
# range(start, stop, step) BUILDS that sequence of numbers:
#   - starts AT 'start'
#   - stops BEFORE 'stop'  (stop is never included!)
#   - jumps by 'step' each time
#
# We draw one colored dot per value, so the sequence range()
# produced becomes a visible row. Change the numbers at the top
# and predict the row before you run it.
# ============================================================

import turtle

START = 0
STOP  = 20      # NOTE: 20 is NOT included
STEP  = 2

screen = turtle.Screen()
screen.bgcolor("black")
screen.title(f"for i in range({START}, {STOP}, {STEP})")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

x = -260
# ---- the loop -------------------------------------------------
for i in range(START, STOP, STEP):
    # TRACE: this is the value the loop is holding right now
    print(f"i = {i:2d}  -> draw dot #{(i - START) // STEP + 1}")

    pen.goto(x, 0)
    pen.dot(20, "lime")
    pen.goto(x, -25)
    pen.color("white")
    pen.write(i, align="center", font=("Arial", 12, "bold"))
    x += 36

print(f"\nrange({START}, {STOP}, {STEP}) produced these values. {STOP} was skipped (stop is exclusive).")
screen.exitonclick()
