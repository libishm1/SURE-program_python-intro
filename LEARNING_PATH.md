# From Syntax to Intent — the learning path

The goal of this repo is not just "learn Python." It's to walk a specific arc:

> **Start by writing syntax** (the literal mechanics of a program) →
> **end by expressing intent** (describe *what* you want, and let the program work
> out *how*).

That shift — from spelling out every step to stating a goal and trusting a solver
to realize it — is the most important transition in modern programming. The files
in this repo are arranged to take you across it.

```
   SYNTAX                COMPOSITION                 INTENT
   how a line works  ►   combine lines into  ►   state a goal; a solver/
   (loops, ifs,          a program that          optimiser figures out
    lists, dicts)        does something          the "how"
   teaching_basics/      turtle / plots / CV     robot CAM toolpaths
```

---

## Stage 1 — Syntax: make the invisible visible

**Where:** [teaching_basics/](teaching_basics/)

You learn what each construct *does*, one at a time, by **watching state change**:
a `while` loop's counter, an `if/elif` branch decision, a list growing and
shrinking, a dictionary mapping keys to values. Every lesson prints a trace that
matches a debugger's variable panel.

At this stage **you are the computer's brain** — you say exactly what happens on
every step. The skill being built: reading code as a sequence of state changes.

> Key idea: *a program has state, and state changes one step at a time.*

---

## Stage 2 — Composition: combine syntax into something that does a job

**Where:** the standalone scripts —
[plot_a_parabola.py](plot_a_parabola.py), [Hilbert.py](Hilbert.py),
[draw_hexagon.py](draw_hexagon.py), [heptagon.py](heptagon.py),
[image_tracing.py](image_tracing.py), [smile.py](smile.py),
[cam_toolpath_paraboloid.py](cam_toolpath_paraboloid.py).

Now you assemble loops, math, and library calls into a small program with a
purpose: draw a curve, trace an image, render a 3D toolpath. You still control the
"how" — but you're starting to think in terms of an outcome ("draw a paraboloid
spiral") rather than individual statements.

> Key idea: *syntax is a means to an end; the end is a result you can describe.*

---

## Stage 3 — Intent: describe the goal, let the program solve it

**Where:** the robot CAM scripts —
[robot_hand_simulation.py](robot_hand_simulation.py),
[robot_spiral_toolpath.py](robot_spiral_toolpath.py),
[robot_zigzag_toolpath.py](robot_zigzag_toolpath.py).

This is the destination. You no longer hand-compute the answer — you **state intent
and a solver realizes it**:

| You express (intent) | The program figures out (how) |
|----------------------|-------------------------------|
| "Put the tool tip *here* in 3D" | Inverse kinematics solves the joint angles |
| "Machine this dome part" | A spiral / zig-zag toolpath is generated over the surface |
| "Keep the path within the arm's reach and executable" | `optimise_placement()` scales and positions the part automatically |
| "Don't let the arm dance around" | The optimiser is biased toward gentle, reachable motion |

You can see the transition *inside* the code itself: the original
`robot_hand_simulation.py` used a **heuristic IK** — hand-tuned fudge factors that
roughly point the arm. That's still "syntax thinking": you wrote the how. The
`robot_spiral_toolpath.py` rewrite replaced it with a **real analytic IK** — you
declare the target point and the math *guarantees* the tool lands there. Same goal,
but now expressed as intent.

> Key idea: *you describe the outcome and the constraints; the program is
> responsible for finding a correct "how."*

---

## Why this matters

The trajectory in this repo mirrors where programming is going. Whether the solver
is inverse kinematics, an optimiser, or an AI assistant, the valuable skill is the
same:

1. **Know the syntax** well enough to read and trust what runs (Stage 1).
2. **Think in outcomes**, decomposing a goal into pieces (Stage 2).
3. **Express intent precisely** — state the goal *and the constraints* clearly
   enough that a solver can satisfy them, then verify the result (Stage 3).

Stage 3 doesn't work without Stage 1. You can only trust a solver's "how" if you
can read it. That's why this repo starts with making state visible and ends with
handing the "how" to a solver — **with you still able to check its work.**

---

## How to travel the path

1. Run the [teaching_basics/](teaching_basics/) lessons in order; predict each
   trace before it prints.
2. Read a Stage 2 script and change one constant at the top — connect a number to
   a visible effect.
3. Read [robot_spiral_toolpath.py](robot_spiral_toolpath.py) and find the line
   where **intent** (`solve_ik(target)`) replaces hand-computed angles. That single
   substitution is the whole point of the course.

See the main [README](README.md) for the file map, and
[GITHUB_WORKFLOW.md](GITHUB_WORKFLOW.md) for saving your work as you go.
