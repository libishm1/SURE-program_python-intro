# ============================================================
# CONCEPT: if / elif / else  (branching / decisions)
# ============================================================
# A program "decides" by testing conditions in ORDER, top to bottom.
# The FIRST branch whose test is True wins; the rest are skipped.
# Order matters: the divisible-by-15 test MUST come before 3 and 5.
#
# We visualise the classic FizzBuzz so each decision becomes a
# colored dot. Reading the colors = reading the branches taken.
# ============================================================

import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("if / elif / else  ->  visual FizzBuzz")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

start_x = -260
y       = 0

for n in range(1, 31):
    # ---- the decision -------------------------------------
    if n % 15 == 0:           # divisible by BOTH 3 and 5
        label, color = "FizzBuzz", "magenta"
    elif n % 3 == 0:          # divisible by 3
        label, color = "Fizz", "deepskyblue"
    elif n % 5 == 0:          # divisible by 5
        label, color = "Buzz", "orange"
    else:                     # none of the above
        label, color = str(n), "gray"

    # TRACE: show which branch was taken (this is the dataflow)
    print(f"n = {n:2d} -> {label}")

    # ---- visualise the branch as a colored dot ------------
    pen.goto(start_x + (n - 1) * 18, y)
    pen.dot(16, color)

# a tiny legend
legend = [("3 -> Fizz", "deepskyblue"), ("5 -> Buzz", "orange"),
          ("15 -> FizzBuzz", "magenta"), ("other -> number", "gray")]
for i, (text, color) in enumerate(legend):
    pen.goto(-260, -40 - i * 24)
    pen.dot(16, color)
    pen.goto(-240, -50 - i * 24)
    pen.color("white")
    pen.write(text, font=("Arial", 12, "normal"))

screen.exitonclick()
