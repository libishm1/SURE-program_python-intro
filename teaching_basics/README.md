# Teaching Basics — visual Python fundamentals

Small, self-contained scripts that make the **invisible parts of a program visible**:
loop counters, branch decisions, and data-structure state — shown both on screen
(turtle) and as a printed **trace** that matches what a debugger's variable panel shows.

Each file teaches exactly one idea. Run them one at a time.

## The lessons (run in order)

| File | Concept | What students watch |
|------|---------|---------------------|
| `01_while_loop.py` | **while loop** | A square spirals out *while* `side < MAX`. The loop variable, its step, and the condition are printed each pass. Comment out the `side += step` line to demonstrate an infinite loop. |
| `02_if_conditions.py` | **if / elif / else** | Visual FizzBuzz — each number becomes a colored dot showing which branch was taken. Teaches that order matters (15 before 3 and 5). |
| `03_lists.py` | **lists** | A list drawn as a bar chart that redraws after every `append` / `pop` / `sort`. The picture and the printed list always match. |
| `04_stack_vs_queue.py` | **stack vs queue** | Same items pushed into both; removal shows LIFO vs FIFO order side by side. |
| `05_cube_3d.py` | **data structures + loops + 3D** | A spinning cube built from a list of vertices and a list of edges. Connects to `../cam_toolpath_paraboloid.py`. |
| `06_debug_dataflow.py` | **debugging dataflow** | Has a deliberate bug that crashes with `ZeroDivisionError`. Students trace the bad value back to its source instead of guessing — the crash is *downstream* of the real cause. |
| `07_for_loop.py` | **for loop + range()** | One dot per value in `range(start, stop, step)`; shows the sequence range builds and that `stop` is excluded. |
| `08_dictionary.py` | **dictionary** | Key→value pairs drawn as labeled boxes; redraws on add, update (same key replaces, not duplicates), and lookup. |

## How to teach debugging with these (VS Code)

1. **Print-tracing first.** Every script prints a trace. Run it and read the trace
   line-by-line next to the code. This builds the mental model of "the program has
   state, and state changes one step at a time."

2. **Then the debugger.** Open `06_debug_dataflow.py`:
   - Click in the gutter on the line marked `# <-- breakpoint here` to set a red dot.
   - Press **F5** (Run and Debug → Python File).
   - When it pauses, look at the **Variables** panel — you'll see `total` is correct
     but `count` is `0`. That mismatch *is* the bug.
   - Use **Step Over (F10)** to walk one line at a time and watch values change.

3. **The big idea — dataflow.** A bug usually shows up *downstream* of its cause
   (the crash is at the division, but the real problem is the missing `count += 1`).
   Debugging = follow the wrong value back to the last place it was right.

## Suggested classroom flow

- Run a script, **predict** the output before it finishes, then check.
- Change ONE constant at the top (e.g. `MAX_SIDE`, `TURNS`) and predict the effect.
- Break it on purpose (remove the loop step, swap `elif` order) and watch it fail.
- Fix `06_debug_dataflow.py` live using a breakpoint.

## Running

```bash
python teaching_basics/01_while_loop.py
```

Turtle windows close on click. `06_debug_dataflow.py` runs in the terminal only.
