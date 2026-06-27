# ============================================================
# CONCEPT: data structures DESCRIBE a 3D object + loops draw it
# ============================================================
# A cube is just DATA:
#   vertices = a list of 8 points  (x, y, z)
#   edges    = a list of 12 pairs of vertex INDEXES to connect
# To draw it we LOOP over the edges and project each 3D point to
# 2D (turtle is flat). To spin it we LOOP applying a rotation.
#
# This connects everything: lists hold the model, for-loops walk
# the lists, and a little math turns 3D into something drawable.
# (Same projection idea as cam_toolpath_paraboloid.py.)
# ============================================================

import math
import time
import turtle

# ---- the model: pure data -------------------------------------
S = 120
vertices = [
    (-S, -S, -S), (S, -S, -S), (S, S, -S), (-S, S, -S),   # back face  0..3
    (-S, -S,  S), (S, -S,  S), (S, S,  S), (-S, S,  S),   # front face 4..7
]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),   # back square
    (4, 5), (5, 6), (6, 7), (7, 4),   # front square
    (0, 4), (1, 5), (2, 6), (3, 7),   # connecting struts
]

# ---- screen ---------------------------------------------------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("a cube = list of vertices + list of edges")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.pensize(2)


def rotate(point, ax, ay):
    """Rotate a 3D point around the X then Y axis."""
    x, y, z = point
    # rotate around X
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    # rotate around Y
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    return x, y, z


def project(point):
    """3D -> 2D with simple perspective (far points shrink)."""
    x, y, z = point
    f = 300 / (300 + z)        # things farther away (larger z) get smaller
    return x * f, y * f


# ---- the animation loop ---------------------------------------
angle = 0.0
print("Drawing a cube from", len(vertices), "vertices and", len(edges), "edges.")
print("Each frame: rotate every vertex, then loop edges to connect them.")

for frame in range(240):
    angle += 0.04
    # 1) transform: rotate every vertex (loop over the data structure)
    moved = [rotate(v, angle, angle * 0.7) for v in vertices]
    # 2) flatten: project each to 2D
    screen_pts = [project(p) for p in moved]

    # 3) draw: loop the edge list, connect the two indexed points
    pen.clear()
    for a, b in edges:
        pen.penup()
        pen.goto(screen_pts[a])
        pen.pendown()
        pen.color("cyan")
        pen.goto(screen_pts[b])

    screen.update()
    time.sleep(0.02)

screen.exitonclick()
