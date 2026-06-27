# Zig-zag (raster / boustrophedon) CAM toolpath on the inverted paraboloid dome.
#
# This is the SECOND strategy.  It reuses everything learned in
# robot_spiral_toolpath.py -- the robot model, real analytic IK/FK, the inverted
# dome surface, the scale, and the reach-aware placement optimiser -- and only
# swaps the toolpath generator: instead of a spiral, the tool sweeps back and
# forth across the dome footprint in parallel rows (a raster pattern), climbing
# and descending the surface as it goes.
#
# Strictly an offline simulation (no camera).
# Run:  python robot_zigzag_toolpath.py
#
import math
import numpy as np
import matplotlib.pyplot as plt

# Reuse the robot + dome "learnings" from the spiral script ------------------
import robot_spiral_toolpath as rs
from robot_spiral_toolpath import (
    norm_surface_z, place, solve_ik, forward_kinematics,
    draw_wireframe, color_ramp, optimise_placement,
    D1, REACH_MIN, REACH_MAX,
)

# ----------------------------------------------------------------------------
# Zig-zag toolpath, in NORMALISED coords (footprint radius = 1, unit disk)
# ----------------------------------------------------------------------------
STEPOVER = 0.16              # spacing between raster rows (across the part)
STEP = 0.06                  # point spacing along each row
ROW_LIMIT = 0.94            # clip rows to |y| <= this so they aren't zero-width


def normalized_zigzag():
    """Boustrophedon raster over the unit disk, draped on the dome surface.

    Returns (nx, ny, nz, t) points; alternate rows reverse direction so the
    tool turns at the ends instead of flying back across the part.
    """
    n_rows = int(2 * ROW_LIMIT / STEPOVER)
    ys = [-ROW_LIMIT + i * STEPOVER for i in range(n_rows + 1)]

    raw = []
    for j, ny in enumerate(ys):
        xmax = math.sqrt(max(0.0, 1.0 - ny * ny))   # disk clip for this row
        if xmax < STEP:
            continue
        n = max(1, int(2 * xmax / STEP))
        xs = [-xmax + k * (2 * xmax / n) for k in range(n + 1)]
        if j % 2 == 1:                               # zig-zag: reverse odd rows
            xs.reverse()
        for nx in xs:
            raw.append((nx, ny))

    total = max(1, len(raw) - 1)
    return [(nx, ny, norm_surface_z(nx, ny), i / total)
            for i, (nx, ny) in enumerate(raw)]


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    zigzag_n = normalized_zigzag()

    # Same placement optimiser / scale as the spiral script ------------------
    scale, (cx, cy, cz), worst = optimise_placement(zigzag_n)
    world_path = [place(nx, ny, scale, cx, cy, cz) for nx, ny, _, _ in zigzag_n]
    ts = [t for *_, t in zigzag_n]

    solutions = [solve_ik(p) for p in world_path]
    n_reach = sum(1 for *_, ok in solutions if ok)

    print("=" * 60)
    print("Zig-zag (raster) toolpath optimisation")
    print("=" * 60)
    print(f"Reach shell (from shoulder) : {REACH_MIN:.2f} .. {REACH_MAX:.2f} m")
    print(f"Dome footprint radius (scale): {scale:.2f} m  (inverted, on table)")
    print(f"Dome centre on workspace     : ({cx:.2f}, {cy:.2f}, {cz:.2f}) m")
    print(f"Raster rows / points         : "
          f"{int(2 * ROW_LIMIT / STEPOVER) + 1} rows, {len(world_path)} points")
    print(f"Worst-point reach margin     : {worst:+.3f} m")
    print(f"Reachable toolpath points    : {n_reach}/{len(world_path)}")
    print(f"Executable                   : {'YES' if n_reach == len(world_path) else 'NO'}")
    print("=" * 60)

    # Animate the arm running the raster pattern ------------------------------
    plt.ion()
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")

    traced = []
    for idx, (sol, p) in enumerate(zip(solutions, world_path)):
        links = np.array(forward_kinematics(*sol[:3]))
        traced.append(p)

        ax.clear()
        draw_wireframe(ax, scale, cx, cy, cz)

        tr = np.array(traced)
        for k in range(1, len(tr)):
            ax.plot(tr[k - 1:k + 1, 0], tr[k - 1:k + 1, 1], tr[k - 1:k + 1, 2],
                    color=color_ramp(ts[k]), lw=2.2)

        ax.plot(links[:, 0], links[:, 1], links[:, 2],
                "-o", color="#d0d0d0", mfc="#1e90ff", lw=3, ms=6)
        ax.scatter(*links[-1], color="red", s=60)

        ax.set_xlim(-0.4, 1.8)
        ax.set_ylim(-1.1, 1.1)
        ax.set_zlim(0.0, 1.6)
        ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
        ax.set_title(f"Robot machining dome zig-zag  ({idx + 1}/{len(world_path)})")
        ax.view_init(elev=22, azim=-60)
        plt.draw(); plt.pause(0.001)

    print("Toolpath complete. Close the window to exit.")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
