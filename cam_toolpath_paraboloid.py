# Build a 3D CAM toolpath with turtle:
#   1. plot a paraboloid surface (z = a*(x^2 + y^2)) in 3D
#   2. discretize it into a grid of points (wireframe)
#   3. draw a spiral toolpath that descends onto the surface
#
# Turtle is 2D, so every 3D point (x, y, z) is flattened to the screen
# with a simple isometric projection.

import math
import turtle

# ---- surface / toolpath parameters -------------------------------------
R       = 200      # radius of the paraboloid footprint
CURV    = 0.0035   # curvature 'a' in z = a*(x^2 + y^2); bigger = deeper bowl
SCALE_Z = 1.0      # vertical exaggeration for the drawing
TURNS   = 8        # how many revolutions the spiral toolpath makes
GRID_R  = 6        # number of rings in the wireframe grid
GRID_A  = 24       # number of spokes in the wireframe grid

# ---- isometric projection: 3D point -> 2D screen point -----------------
ISO = math.radians(30)
def project(x, y, z):
    sx = (x - y) * math.cos(ISO)
    sy = (x + y) * math.sin(ISO) - z * SCALE_Z
    return sx, sy

def surface_z(x, y):
    return CURV * (x * x + y * y)

# ---- turtle setup ------------------------------------------------------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("3D CAM toolpath on a paraboloid")
screen.tracer(0, 0)          # turn off animation -> draw instantly, then update once

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

def goto3d(x, y, z):
    sx, sy = project(x, y, z)
    pen.goto(sx, sy)

def move3d(x, y, z):
    sx, sy = project(x, y, z)
    pen.penup()
    pen.goto(sx, sy)
    pen.pendown()

# ---- 1+2: draw the discretized paraboloid as a wireframe grid ----------
pen.pencolor("#3a4a5a")
pen.pensize(1)

# concentric rings
for i in range(1, GRID_R + 1):
    r = R * i / GRID_R
    first = True
    for a in range(GRID_A + 1):
        theta = 2 * math.pi * a / GRID_A
        x, y = r * math.cos(theta), r * math.sin(theta)
        z = surface_z(x, y)
        if first:
            move3d(x, y, z)
            first = False
        else:
            goto3d(x, y, z)

# radial spokes
for a in range(GRID_A):
    theta = 2 * math.pi * a / GRID_A
    first = True
    for i in range(GRID_R + 1):
        r = R * i / GRID_R
        x, y = r * math.cos(theta), r * math.sin(theta)
        z = surface_z(x, y)
        if first:
            move3d(x, y, z)
            first = False
        else:
            goto3d(x, y, z)

# ---- 3: spiral toolpath descending from the rim to the center ----------
def color_ramp(t):
    # t in [0,1] -> warm gradient (yellow -> orange -> red)
    r = 1.0
    g = max(0.0, 1.0 - t)
    b = max(0.0, 0.3 - 0.3 * t)
    return (r, g, b)

screen.colormode(1.0)
pen.pensize(3)

STEPS = TURNS * GRID_A * 2
first = True
for s in range(STEPS + 1):
    t = s / STEPS                      # 0 at rim, 1 at center
    r = R * (1 - t)                    # spiral inward
    theta = TURNS * 2 * math.pi * t    # wind around
    x, y = r * math.cos(theta), r * math.sin(theta)
    z = surface_z(x, y)

    pen.pencolor(color_ramp(t))
    if first:
        move3d(x, y, z)
        first = False
    else:
        goto3d(x, y, z)

screen.update()
screen.exitonclick()
