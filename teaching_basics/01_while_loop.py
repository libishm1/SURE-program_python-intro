# ============================================================
# CONCEPT: the while loop
# ============================================================
# A while loop repeats a block AS LONG AS a condition is True.
# The three things to watch (these are what a debugger shows you):
#   1. the loop variable        -> 'side'
#   2. how it CHANGES each pass  -> side += step
#   3. the CONDITION it is tested against -> side < MAX_SIDE
#
# If the variable never moves toward making the condition False,
# the loop runs forever. That is the #1 bug to teach.
# ============================================================

import turtle

MAX_SIDE = 200        # stop once the square's side reaches this
side     = 20         # the loop variable (start small)
step     = 12         # how much it grows each pass
angle    = 91         # 91 (not 90) makes the squares spiral nicely

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("while loop: keep drawing WHILE side < MAX")

pen = turtle.Turtle()
pen.color("cyan")
pen.speed(3)          # slow enough to WATCH the loop happen

iteration = 0
# ---- the loop -------------------------------------------------
while side < MAX_SIDE:
    iteration += 1

    # TRACE: this printout mirrors a debugger 'watch' window.
    keep_going = side < MAX_SIDE
    print(f"pass {iteration:2d} | side = {side:3d} | side < {MAX_SIDE}? {keep_going} -> draw")

    # draw one square
    for _ in range(4):
        pen.forward(side)
        pen.right(angle)

    side += step      # <-- THE STEP. Remove this line => infinite loop!

# ---- after the loop -------------------------------------------
print(f"\nLOOP ENDED: side = {side}, which is NOT < {MAX_SIDE}. Condition is now False.")

pen.hideturtle()
screen.exitonclick()
