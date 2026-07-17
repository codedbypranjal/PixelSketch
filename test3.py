import cv2
import numpy as np

# Load your target image
# IMAGE_PATH = "satyasai.jpg"
IMAGE_PATH = "anandji.jpg"
img = cv2.imread(IMAGE_PATH)

# Getting original height and width
orig_h, orig_w = img.shape[:2]
max_display_dim = 700
# Calculate scale factor without losing original structural proportions
scale = max_display_dim / max(orig_h, orig_w)
new_w = int(orig_w * scale)
new_h = int(orig_h * scale)
img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

# Convert to gray and use mild blurring to retain thin features
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# Tightened thresholds (lower CANNY_LOW catches fine details/shadow transitions)
edges = cv2.Canny(blurred, 35, 125)

# Use CHAIN_APPROX_NONE to preserve every structural point for organic looking lines
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Save the structural coordinates map file
with open("detailed_strokes.txt", "w") as f:
    # Save the custom drawing dimensions as the first header row
    f.write(f"CANVAS_DIMENSIONS {new_w},{new_h}\n")

    for contour in contours:
        # Lower limit allows shorter detailed accent lines to pass through
        if cv2.arcLength(contour, closed=False) > 10:
            start_x, start_y = contour[0][0]
            bgr_color = img[int(start_y), int(start_x)]
            r, g, b = bgr_color[2] / 255.0, bgr_color[1] / 255.0, bgr_color[0] / 255.0

            f.write(f"STROKE {r},{g},{b}\n")
            for point in contour:
                x, y = point[0]
                f.write(f"{x},{y}\n")
            f.write("END_STROKE\n")

print(f"Success! Captured detailed strokes maintaining a ratio of {new_w}x{new_h}.")