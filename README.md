# Summer Courses — Python, CAM toolpaths & a robot-arm simulation

A collection of small, self-contained Python scripts from a summer course: turtle
graphics, plotting, computer vision, and a set of scripts that build CAM toolpaths
and run them on a simulated 6-DOF robot arm.

Everything here is an **offline simulation or a local visual** — nothing talks to
real hardware.

> **The point of this repo:** travel from **syntax** (the literal mechanics of code)
> to **intent** (describe a goal; let a solver work out the *how*). Read
> [LEARNING_PATH.md](LEARNING_PATH.md) first — it explains how the files are
> arranged to take you across that transition.

## Setup

```bash
pip install -r requirements.txt
```

Requires Python 3.9+. Most scripts open a window (matplotlib or turtle); a few use
the webcam. See [requirements.txt](requirements.txt) for what each package is for.

New to git/GitHub? See the [GitHub workflow cheat sheet](GITHUB_WORKFLOW.md) for how
to `add`, `commit`, and `push` your changes.

---

## Robot arm + CAM toolpaths (the main project)

A UR10e-like 6-DOF arm whose end-effector executes machining toolpaths over a
paraboloid part. The toolpath is **optimised so every point lands inside the arm's
reach** and the motion stays gentle.

| File | What it does |
|------|--------------|
| [robot_hand_simulation.py](robot_hand_simulation.py) | The original sim: the arm's end-effector follows a face/hand tracked by the **webcam**. Forward kinematics + a heuristic IK. The starting point for everything below. |
| [cam_toolpath_paraboloid.py](cam_toolpath_paraboloid.py) | The original CAM demo: draws a **spiral toolpath descending over a paraboloid** bowl, in 2D turtle with an isometric projection. |
| [robot_spiral_toolpath.py](robot_spiral_toolpath.py) | **Combined + optimised.** Generates the paraboloid spiral, inverts it into a small **dome that sits on the table in front of the robot**, auto-places it so the whole path is reachable, and drives the arm along it with a **real analytic IK** (tool tip lands exactly on each point). Strictly offline (no camera). |
| [robot_zigzag_toolpath.py](robot_zigzag_toolpath.py) | **Second strategy.** A zig-zag (raster / boustrophedon) toolpath over the same dome. Imports the robot model, IK/FK, dome surface, scale, and placement optimiser from `robot_spiral_toolpath.py` — only the path pattern differs. |

### Run them

```bash
python robot_spiral_toolpath.py     # spiral toolpath on the dome
python robot_zigzag_toolpath.py     # zig-zag toolpath on the dome
python robot_hand_simulation.py     # webcam face-following demo
```

Each toolpath script prints a reach/optimisation report, then animates the arm
machining the part in 3D. Close the window to exit.

### How it fits together

```
cam_toolpath_paraboloid.py  ─┐
                             ├─►  robot_spiral_toolpath.py  ──►  robot_zigzag_toolpath.py
robot_hand_simulation.py    ─┘    (shared robot + dome core)     (imports the core)
```

`robot_spiral_toolpath.py` holds the reusable core — `solve_ik`, `forward_kinematics`,
the inverted-dome surface, the `TARGET_SCALE`, and `optimise_placement()`. The
zig-zag script and any future pattern just plug a new toolpath generator into it.

> **Next step (planned):** make the toolpath *adaptive* — let the camera define or
> warp the dome surface, and re-run `optimise_placement()` each frame to keep the
> path reachable. The code is already structured for this; the optimiser and IK are
> pure functions you can call per-frame.

---

## Other scripts

| File | What it does |
|------|--------------|
| [plot_a_parabola.py](plot_a_parabola.py) | Plots a parabola with matplotlib. |
| [image_tracing.py](image_tracing.py) | Traces edges/contours of an image with OpenCV. |
| [smile.py](smile.py) | OpenCV face/smile demo. |
| [Hilbert.py](Hilbert.py) | Hilbert space-filling curve (turtle). |
| [draw_hexagon.py](draw_hexagon.py) | Hexagon pattern (turtle). |
| [heptagon.py](heptagon.py) | Heptagon (turtle). |
| [addition.py](addition.py) | Basic arithmetic example. |

## Teaching materials

[teaching_basics/](teaching_basics/) is a separate mini-course on Python
fundamentals (loops, conditions, lists, stacks/queues, dictionaries, debugging),
each lesson made visible with turtle graphics. It has its own
[README](teaching_basics/README.md).

---

## Notes

- **Windows:** these were developed on Windows 11. Use `python` (or `py`) to run.
- **Webcam scripts** (`robot_hand_simulation.py`, `smile.py`) fall back gracefully
  if no camera or MediaPipe is available.
- The robot scripts are pure simulation — safe to run anywhere, no hardware needed.
