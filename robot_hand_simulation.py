# Simulate a UR10e-like robot arm whose end effector follows a hand position.
import math
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

try:
    import mediapipe as mp
except Exception as exc:
    mp = None
    print(f"MediaPipe unavailable: {exc}. Falling back to a simple camera tracker.")

fig = plt.figure(figsize=(15, 5))
ax3d = fig.add_subplot(131, projection='3d')
ax2d = fig.add_subplot(132)
ax_cam = fig.add_subplot(133)
ax_cam.set_axis_off()

if mp is not None:
    try:
        mp_face = mp.solutions.face_detection
        face_detector = mp_face.FaceDetection(min_detection_confidence=0.7)
    except AttributeError:
        face_detector = None
        print("MediaPipe face detection is unavailable; using a simple fallback tracker.")
else:
    face_detector = None


def clamp(value, low, high):
    return max(low, min(high, value))


def smooth_target(current, target, alpha=0.25):
    return (
        current[0] + alpha * (target[0] - current[0]),
        current[1] + alpha * (target[1] - current[1]),
        current[2] + alpha * (target[2] - current[2]),
    )


PARKED_POSE = [
    math.radians(-90),  # θ1 — base pan (arm faces the camera, -Y)
    math.radians(-90),  # θ2 — shoulder: upper arm points straight up
    math.radians(-90),  # θ3 — elbow: forearm horizontal at top
    math.radians(-90),  # θ4 — wrist-1
    math.radians(90),   # θ5 — wrist-2
    math.radians(90),   # θ6 — tool
]


def solve_ur10e_ik(target):
    tx, ty, _ = target

    base_delta = clamp(tx * 0.90, -math.radians(70), math.radians(70))
    shoulder_delta = clamp(ty * 0.80, -math.radians(60), math.radians(60))
    elbow_delta = clamp(-ty * 0.60, -math.radians(60), math.radians(60))
    wrist_yaw_delta = clamp(-tx * 0.60, -math.radians(60), math.radians(60))

    base_angle = PARKED_POSE[0] + base_delta
    shoulder_angle = PARKED_POSE[1] + shoulder_delta
    elbow_angle = PARKED_POSE[2] + elbow_delta
    wrist_yaw = PARKED_POSE[3] + wrist_yaw_delta
    wrist_pitch = PARKED_POSE[4]
    wrist_roll = PARKED_POSE[5]

    return [base_angle, shoulder_angle, elbow_angle, wrist_yaw, wrist_pitch, wrist_roll]


def forward_kinematics(joint_angles):
    """3-D FK for a UR10e-like 6-DOF arm using proper rotation matrices.

    Joint convention (UR-compatible):
      θ1 — base pan   (Z rotation)
      θ2 — shoulder   (Y in joint-1 frame); -90° → upper arm points up
      θ3 — elbow      (Y cumulative);       -90° → forearm horizontal
      θ4 — wrist-1    (X in joint-3 frame)
      θ5 — wrist-2    (Y in joint-4 frame)
      θ6 — tool roll  (X, only affects orientation, last point unchanged)

    At PARKED_POSE [90,-90,-90,-90,90,90] deg the arm stands vertically on its
    base then bends 90° at the top — the standard UR upright home position.
    """
    D1  = 0.28   # base-to-shoulder height
    A2  = 0.90   # upper-arm length
    A3  = 0.85   # forearm length
    D4  = 0.25   # wrist-1 offset along forearm axis
    D5  = 0.12   # wrist-2 offset
    D6  = 0.10   # tool length

    def Rz(a):
        c, s = math.cos(a), math.sin(a)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    def Ry(a):
        c, s = math.cos(a), math.sin(a)
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    def Rx(a):
        c, s = math.cos(a), math.sin(a)
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

    t = joint_angles
    ex = np.array([1.0, 0.0, 0.0])   # local "forward" unit vector

    positions = [(0.0, 0.0, 0.0)]

    # Base column: joint 1 only rotates the arm plane, doesn't move shoulder height
    shoulder = np.array([0.0, 0.0, D1])
    positions.append(tuple(shoulder))

    # Shoulder + elbow (joints 1-2)
    R = Rz(t[0]) @ Ry(t[1])
    fwd = R @ ex
    elbow = shoulder + A2 * fwd
    positions.append(tuple(elbow))

    # Wrist-1 (joint 3)
    R = R @ Ry(t[2])
    fwd = R @ ex
    wrist1 = elbow + A3 * fwd
    positions.append(tuple(wrist1))

    # Wrist-2 (joint 4 — roll, offset continues along forearm direction)
    R = R @ Rx(t[3])
    wrist2 = wrist1 + D4 * fwd
    positions.append(tuple(wrist2))

    # Wrist-3 (joint 5 — pitch)
    R = R @ Ry(t[4])
    fwd = R @ ex
    wrist3 = wrist2 + D5 * fwd
    positions.append(tuple(wrist3))

    # Tool (joint 6 — roll, position only changes direction not magnitude here)
    R = R @ Rx(t[5])
    fwd = R @ ex
    tool = wrist3 + D6 * fwd
    positions.append(tuple(tool))

    return positions


def update_plot(joint_angles):
    ax3d.clear()
    positions = forward_kinematics(joint_angles)

    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    zs = [p[2] for p in positions]

    ax3d.plot(xs, ys, zs, marker='o')
    ax3d.set_xlim([-2.2, 2.2])
    ax3d.set_ylim([-2.2, 2.2])
    ax3d.set_zlim([0.0, 2.2])
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.view_init(elev=20, azim=35)
    plt.draw()
    plt.pause(0.01)


def update_2d_plot(face_xy, mapped_target):
    ax2d.clear()
    ax2d.set_xlim(0, 1)
    ax2d.set_ylim(1, 0)
    ax2d.set_aspect('equal')
    ax2d.set_title('Face position -> end effector target')
    ax2d.axvline(0.5, color='gray', alpha=0.4)
    ax2d.axhline(0.5, color='gray', alpha=0.4)

    if face_xy is not None:
        ax2d.scatter(face_xy[0], face_xy[1], color='red', s=70, label='face')

    target_x = clamp((mapped_target[0] / 0.35 + 1.0) * 0.5, 0.0, 1.0)
    target_y = clamp((0.5 - mapped_target[1] / 0.25) * 0.5 + 0.5, 0.0, 1.0)
    ax2d.scatter(target_x, target_y, color='lime', s=70, label='target')
    ax2d.legend(loc='upper right')
    plt.draw()


def update_camera_view(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ax_cam.clear()
    ax_cam.imshow(frame_rgb)
    ax_cam.set_title('Camera View')
    ax_cam.set_axis_off()
    plt.draw()


def detect_face_position(frame):
    if face_detector is not None:
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detector.detect(frame_rgb)
            if results:
                detection = results[0]
                location = detection.location_data.relative_bounding_box
                cx = location.xmin + location.width / 2.0
                cy = location.ymin + location.height / 2.0
                return (float(cx), float(cy))
        except Exception:
            pass

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 40, 80], dtype=np.uint8)
    upper = np.array([25, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.medianBlur(mask, 5)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) > 300:
            moments = cv2.moments(contour)
            if moments['m00'] != 0:
                cx = moments['m10'] / moments['m00']
                cy = moments['m01'] / moments['m00']
                cv2.circle(frame, (int(cx), int(cy)), 8, (0, 255, 0), -1)
                return (cx / frame.shape[1], cy / frame.shape[0])

    return None


def map_face_to_target(face_xy, previous_target):
    if face_xy is None:
        return previous_target

    x_norm, y_norm = face_xy
    x = clamp((x_norm - 0.5) * 2.0, -1.0, 1.0)
    y = clamp((0.5 - y_norm) * 2.0, -1.0, 1.0)

    target = (
        x * 0.60,
        y * 0.40,
        1.15,
    )
    return smooth_target(previous_target, target, alpha=0.6)


def main():
    plt.ion()
    plt.show(block=False)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No webcam detected; using a small demo target instead.")
        cap = None

    joint_angles = PARKED_POSE.copy()
    target = (0.0, 0.0, 1.15)

    while True:
        if cap is not None:
            ret, frame = cap.read()
            if not ret:
                break
            face_xy = detect_face_position(frame)
            if face_xy is not None:
                target = map_face_to_target(face_xy, target)
            else:
                target = smooth_target(target, (0.0, 0.0, 1.15), alpha=0.1)

            update_camera_view(frame)
            try:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            except Exception:
                pass
        else:
            target = smooth_target(target, (0.0, 0.0, 1.15), alpha=0.1)
            face_xy = None
            time.sleep(0.03)

        joint_angles = solve_ur10e_ik(target)
        update_plot(joint_angles)
        update_2d_plot(face_xy, target)
        time.sleep(0.02)

    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    plt.close(fig)


if __name__ == "__main__":
    main()

    