
import cv2
import numpy as np
from skimage.morphology import skeletonize


def preprocess_fingerprint(image_path):

    # Read fingerprint image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read fingerprint image")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve image contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Remove noise
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # Convert to binary image
    _, binary = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    return binary


def extract_minutiae(binary):

    # Convert binary image into skeleton
    skeleton = skeletonize(binary > 0)

    skeleton = skeleton.astype(np.uint8)

    height, width = skeleton.shape

    minutiae = []

    # Check each pixel
    for y in range(1, height - 1):

        for x in range(1, width - 1):

            if skeleton[y, x] == 0:
                continue

            # Get 8 neighbouring pixels
            neighbours = [
                skeleton[y-1, x],
                skeleton[y-1, x+1],
                skeleton[y, x+1],
                skeleton[y+1, x+1],
                skeleton[y+1, x],
                skeleton[y+1, x-1],
                skeleton[y, x-1],
                skeleton[y-1, x-1]
            ]

            # Calculate crossing number
            crossing_number = sum(
                abs(int(neighbours[i]) -
                    int(neighbours[(i+1) % 8]))
                for i in range(8)
            ) / 2

            # Ridge ending
            if crossing_number == 1:
                minutiae.append((x, y, "ending"))

            # Ridge bifurcation
            elif crossing_number == 3:
                minutiae.append((x, y, "bifurcation"))

    return skeleton, minutiae
