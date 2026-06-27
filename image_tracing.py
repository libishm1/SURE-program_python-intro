import cv2
import numpy as np
from collections import deque

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

# Window and Trackbar setup
cv2.namedWindow('Motion Detection')
cv2.createTrackbar('Threshold', 'Motion Detection', 30, 255, nothing)

# Graph setup
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 240
history = deque(maxlen=GRAPH_WIDTH)

# Read the first frame
ret, prev_frame = cap.read()
if not ret:
    print("Failed to grab the first frame.")
    cap.release()
    exit()

# Get frame dimensions for combined view
frame_height, frame_width, _ = prev_frame.shape

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get threshold from trackbar
    threshold_value = cv2.getTrackbarPos('Threshold', 'Motion Detection')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compute the absolute difference
    frame_diff = cv2.absdiff(prev_gray, gray)

    # Threshold the difference
    _, thresh = cv2.threshold(frame_diff, threshold_value, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours of the motion
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_amount = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 500: # Ignore small movements
            continue
        
        motion_amount += area
        
        # Draw colored contours based on size
        color_value = min(area / 5000, 1.0) # Normalize area for color mapping
        color = (0, int(255 * color_value), int(255 * (1 - color_value)))
        cv2.drawContours(frame, [contour], -1, color, 2)

    # --- Vector Visualization using Optical Flow ---
    # Calculate dense optical flow
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Draw the flow vectors on the frame
    step = 16  # Draw a vector every 16 pixels
    h, w = frame.shape[:2]

    # Create a mask for visualization
    vis_mask = np.zeros_like(frame)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = np.zeros_like(frame)
    hsv[..., 1] = 255
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Draw colored vectors
    for y in range(0, h, step):
        for x in range(0, w, step):
            fx, fy = flow[y, x]
            cv2.line(frame, (x, y), (int(x + fx), int(y + fy)), (int(bgr[y, x][0]), int(bgr[y, x][1]), int(bgr[y, x][2])))
    # Update and draw the graph
    history.append(motion_amount)
    graph = np.zeros((GRAPH_HEIGHT, GRAPH_WIDTH, 3), dtype=np.uint8)
    for i in range(1, len(history)):
        # Map motion amount to color for the graph line
        color_value = min(history[i-1] / 50000, 1.0)
        line_color = (255, int(255 * (1 - color_value)), int(255 * color_value))
        cv2.line(graph, (i - 1, GRAPH_HEIGHT - int(history[i-1] / 100)), (i, GRAPH_HEIGHT - int(history[i] / 100)), line_color, 2)

    # Combine the frame and the graph for display
    combined_view = np.hstack((frame, cv2.resize(graph, (GRAPH_WIDTH, frame_height))))
    cv2.imshow('Motion Detection', combined_view)

    prev_gray = gray # Update the previous frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()