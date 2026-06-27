# Combine the UR10e-like robot arm (robot_hand_simulation.py) with the
# paraboloid CAM spiral (cam_toolpath_paraboloid.py):
#
#   1. generate the descending spiral toolpath over a paraboloid bowl
#   2. OPTIMISE its scale + placement so every toolpath point lands inside
#      the arm's reachable shell (so the path is actually executable)
#   3. drive the robot end-effector along the optimised spiral using a REAL
#      analytic inverse kinematics solver (not the heuristic one in the
#      original sim), and animate the arm tracing the path in 3D.
#
# Run:  python robot_spiral_toolpath.py
#
import math
import time
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Robot model (lengths carried over from robot_hand_simulation.py)
# ----------------------------------------------------------------------------
D1 = 0.28          # base column height (origin -> shoulder)
A2 = 0.90          # upper arm   (shoulder -> elbow)
A3 = 0.85          # forearm     (elbow -> wrist)
D_TOOL = 0.47      # wrist-1 + wrist-2 + tool (0.25 + 0.12 + 0.10), kept colinear

# For positioning IK the forearm + wrist + tool act as one straight final link.
L1 = A2                       # 0.90
L2 = A3 + D_TOOL              # 1.32

SHOULDER = np.array([0.0, 0.0, D1])
REACH_MAX = L1 + L2           # 2.22
REACH_MIN = abs(L2 - L1)      # 0.42
MARGIN = 0.10                 # keep this far inside both reach bounds
Z_FLOOR = 0.05                # don't let the tool dip below the table

# ----------------------------------------------------------------------------
# Paraboloid spiral toolpath, in NORMALISED coords (footprint radius = 1).
# INVERTED: a dome/mound that sits on the table -> peak at centre, base at rim.
#   nz = a * (1 - (x^2 + y^2));  base (rim) at 0, peak at a.
# ----------------------------------------------------------------------------
CURV_N = 0.7                 # dome height as a fraction of its footprint radius
TURNS = 6
GRID_R = 6
GRID_A = 24
STEPS = TURNS * GRID_A        # toolpath sample count

# Where the part lives on the workspace, in front of the robot
TABLE_Z = 0.12               # height of the table the dome sits on
TARGET_SCALE = 0.40          # dome footprint radius (m) -- small, scaled down


def norm_surface_z(nx, ny):
    return CURV_N * (1.0 - (nx * nx + ny * ny))


def normalized_spiral():
    """Return list of (nx, ny, nz, t) spiral points, rim (t=0) -> centre (t=1)."""
    pts = []
    for s in range(STEPS + 1):
        t = s / STEPS
        nr = 1.0 - t
        theta = TURNS * 2 * math.pi * t
        nx, ny = nr * math.cos(theta), nr * math.sin(theta)
        pts.append((nx, ny, norm_surface_z(nx, ny), t))
    return pts


def place(nx, ny, scale, cx, cy, cz):
    """Map a normalised bowl point into world (robot) coordinates."""
    return np.array([
        cx + scale * nx,
        cy + scale * ny,
        cz + scale * norm_surface_z(nx, ny),
    ])


# ----------------------------------------------------------------------------
# Reachability + optimisation
# ----------------------------------------------------------------------------
def point_margin(p):
    """How far point p sits inside the reachable shell (negative = outside)."""
    r = math.hypot(p[0], p[1])
    h = p[2] - D1
    d = math.hypot(r, h)
    shell_margin = min(d - (REACH_MIN + MARGIN), (REACH_MAX - MARGIN) - d)
    floor_margin = p[2] - Z_FLOOR
    return min(shell_margin, floor_margin)


def evaluate(spiral_n, scale, cx, cy, cz):
    """Worst-case margin over all spiral points for a given placement."""
    worst = math.inf
    for nx, ny, _, _ in spiral_n:
        m = point_margin(place(nx, ny, scale, cx, cy, cz))
        if m < worst:
            worst = m
            if worst < -1.0:        # hopeless, bail early
                break
    return worst


def optimise_placement(spiral_n):
    """Place the small dome on the table in front of the robot.

    The dome scale is fixed (scaled down) and it rests on the table (cz fixed),
    so we only search the forward distance cx that keeps the whole toolpath
    comfortably reachable.  Maximising the worst-point margin centres the part
    in the reach shell, which keeps joint motion gentle (no dancing around).
    """
    scale, cz = TARGET_SCALE, TABLE_Z
    COMFORT = 0.05            # required reach margin to consider a spot "safe"
    candidates = []
    for cx in [round(0.55 + 0.05 * i, 2) for i in range(24)]:   # 0.55 .. 1.70
        candidates.append((cx, evaluate(spiral_n, scale, cx, 0.0, cz)))
    # Prefer the FARTHEST safe placement: a part farther in front subtends a
    # smaller azimuth, so the base barely pans -> no dancing around.
    safe = [(cx, m) for cx, m in candidates if m >= COMFORT]
    if safe:
        cx, best_margin = max(safe, key=lambda c: c[0])
    else:
        cx, best_margin = max(candidates, key=lambda c: c[1])
    return scale, (cx, 0.0, cz), best_margin


# ----------------------------------------------------------------------------
# Real analytic inverse kinematics  (base pan + 2-link elbow-up)
# ----------------------------------------------------------------------------
def solve_ik(target):
    """Return (theta1, alpha, elbow_bend, reachable) placing the TOOL TIP on target."""
    tx, ty, tz = target
    theta1 = math.atan2(ty, tx)            # base pan toward the target azimuth
    r = math.hypot(tx, ty)                 # radial distance from base axis
    h = tz - D1                            # height relative to shoulder
    d = math.hypot(r, h)

    reachable = (REACH_MIN <= d <= REACH_MAX)
    d = max(REACH_MIN + 1e-6, min(REACH_MAX - 1e-6, d))   # clamp for safety

    cos_e = (r * r + h * h - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    cos_e = max(-1.0, min(1.0, cos_e))
    elbow_bend = math.acos(cos_e)          # interior bend (elbow-up)

    alpha = math.atan2(h, r) + math.atan2(L2 * math.sin(elbow_bend),
                                          L1 + L2 * math.cos(elbow_bend))
    return theta1, alpha, elbow_bend, reachable


def forward_kinematics(theta1, alpha, elbow_bend):
    """Joint positions: base, shoulder, elbow, wrist, tool-tip."""
    def dir_vec(elev):
        return np.array([math.cos(elev) * math.cos(theta1),
                         math.cos(elev) * math.sin(theta1),
                         math.sin(elev)])

    d1 = dir_vec(alpha)
    elbow = SHOULDER + L1 * d1
    beta = alpha - elbow_bend
    d2 = dir_vec(beta)
    wrist = elbow + A3 * d2
    tip = elbow + L2 * d2
    return [np.zeros(3), SHOULDER, elbow, wrist, tip]


# ----------------------------------------------------------------------------
# Visualisation helpers
# ----------------------------------------------------------------------------
def color_ramp(t):                          # yellow -> orange -> red
    return (1.0, max(0.0, 1.0 - t), max(0.0, 0.3 - 0.3 * t))


def draw_wireframe(ax, scale, cx, cy, cz):
    for i in range(1, GRID_R + 1):          # concentric rings
        rr = i / GRID_R
        pts = [place(rr * math.cos(2 * math.pi * a / GRID_A),
                     rr * math.sin(2 * math.pi * a / GRID_A),
                     scale, cx, cy, cz) for a in range(GRID_A + 1)]
        pts = np.array(pts)
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="#3a4a5a", lw=0.6)
    for a in range(GRID_A):                 # radial spokes
        theta = 2 * math.pi * a / GRID_A
        pts = [place(rr / GRID_R * math.cos(theta), rr / GRID_R * math.sin(theta),
                     scale, cx, cy, cz) for rr in range(GRID_R + 1)]
        pts = np.array(pts)
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="#3a4a5a", lw=0.6)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    spiral_n = normalized_spiral()

    # 1) optimise the spiral so it is reachable & executable -----------------
    scale, (cx, cy, cz), worst = optimise_placement(spiral_n)
    world_path = [place(nx, ny, scale, cx, cy, cz) for nx, ny, _, _ in spiral_n]
    ts = [t for *_, t in spiral_n]

    # pre-solve IK for the whole path and report executability
    solutions = [solve_ik(p) for p in world_path]
    n_reach = sum(1 for *_, ok in solutions if ok)
    rim_d = math.hypot(math.hypot(*world_path[0][:2]), world_path[0][2] - D1)

    print("=" * 60)
    print("Spiral toolpath optimisation")
    print("=" * 60)
    print(f"Reach shell (from shoulder) : {REACH_MIN:.2f} .. {REACH_MAX:.2f} m")
    print(f"Dome footprint radius (scale): {scale:.2f} m  (inverted, on table)")
    print(f"Dome centre on workspace     : ({cx:.2f}, {cy:.2f}, {cz:.2f}) m")
    print(f"Rim distance from shoulder   : {rim_d:.2f} m")
    print(f"Worst-point reach margin     : {worst:+.3f} m")
    print(f"Reachable toolpath points    : {n_reach}/{len(world_path)}")
    print(f"Executable                   : {'YES' if n_reach == len(world_path) else 'NO'}")
    print("=" * 60)

    # 2) animate the arm tracing the optimised spiral ------------------------
    plt.ion()
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")

    traced = []
    for idx, (sol, p, t) in enumerate(zip(solutions, world_path, ts)):
        theta1, alpha, elbow_bend, _ = sol
        links = np.array(forward_kinematics(theta1, alpha, elbow_bend))
        traced.append(p)

        ax.clear()
        draw_wireframe(ax, scale, cx, cy, cz)

        # toolpath traced so far, warm gradient
        tr = np.array(traced)
        for k in range(1, len(tr)):
            ax.plot(tr[k - 1:k + 1, 0], tr[k - 1:k + 1, 1], tr[k - 1:k + 1, 2],
                    color=color_ramp(ts[k]), lw=2.5)

        # the robot arm
        ax.plot(links[:, 0], links[:, 1], links[:, 2],
                "-o", color="#d0d0d0", mfc="#1e90ff", lw=3, ms=6)
        ax.scatter(*links[-1], color="red", s=60)   # tool tip

        ax.set_xlim(-0.4, 1.8)
        ax.set_ylim(-1.1, 1.1)
        ax.set_zlim(0.0, 1.6)
        ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
        ax.set_title(f"Robot machining dome spiral  ({idx + 1}/{len(world_path)})")
        ax.view_init(elev=22, azim=-60)
        plt.draw(); plt.pause(0.001)

    print("Toolpath complete. Close the window to exit.")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
