"""
Marker Detector — Computer Vision Recruitment Task

Implement the MarkerDetector class and the utility functions below.
See README.md for full task description.
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple


class MarkerDetector:
    """
    Detects colored markers in images using classical computer vision techniques.

    Each detection is a dictionary with the following fields:
        - 'color':  str           — one of 'red', 'green', 'blue', 'yellow'
        - 'bbox':   (x, y, w, h) — bounding rectangle of the detected contour
        - 'center': (cx, cy)     — center coordinates of the bounding box
        - 'area':   float        — area of the detected contour

    Optionally, if you attempt the bonus task:
        - 'shape':  str          — one of 'circle', 'triangle', 'rectangle'
    """

    # Define HSV color ranges for each target color.
    # Each entry maps a color name to a list of (lower_bound, upper_bound) tuples.
    # Use np.array([H, S, V]) for bounds. OpenCV uses H: 0-179, S: 0-255, V: 0-255.
    #
    # Hint: Red wraps around the hue spectrum (both ~0-10 and ~170-179 are red),
    # so you will likely need TWO ranges for red.
    COLOR_RANGES = {
        # Example format:
        # "green": [(np.array([35, 80, 80]), np.array([85, 255, 255]))],
        "green":  [(np.array([40, 50, 50]), np.array([85, 255, 255]))],
        "blue":   [(np.array([100, 50, 50]), np.array([140, 255, 255]))],
        "yellow": [(np.array([20, 50, 50]), np.array([35, 255, 255]))],
        "red":    [(np.array([0, 50, 50]), np.array([10, 255, 255])),
                   (np.array([170, 50, 50]), np.array([179, 255, 255]))]
    }

    # Minimum contour area to consider (filters noise)
    min_area = 500

    def detect(self, image: np.ndarray) -> List[Dict]:
        """
        Detect colored markers in the given BGR image.

        Args:
            image: Input image in BGR format (as loaded by cv2.imread).

        Returns:
            A list of detection dictionaries, each containing:
            'color', 'bbox', 'center', and 'area' keys.
        """
        detections = []
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        for color_name, ranges in self.COLOR_RANGES.items():
            color_mask = np.zeros(hsv_img.shape[:2], dtype=np.uint8)
            
            for (lower, upper) in ranges:
                mask = cv2.inRange(hsv_img, lower, upper)
                color_mask = cv2.bitwise_or(color_mask, mask)
                
            contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= self.min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    cx = int(x + w / 2)
                    cy = int(y + h / 2)
                    
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                    vertices = len(approx)
                    
                    if vertices == 3:
                        shape = "triangle"
                    elif vertices == 4:
                        shape = "rectangle"
                    else:
                        shape = "circle"
                    
                    detections.append({
                        'color': color_name,
                        'bbox': (x, y, w, h),
                        'center': (cx, cy),
                        'area': float(area),
                        'shape': shape
                    })
                    
        return detections


def compute_iou(box_a: Tuple, box_b: Tuple) -> float:
    """
    Compute Intersection over Union (IoU) between two bounding boxes.

    Each box is represented as (x, y, w, h) where:
        - (x, y) is the top-left corner
        - (w, h) is the width and height

    Args:
        box_a: First bounding box as (x, y, w, h).
        box_b: Second bounding box as (x, y, w, h).

    Returns:
        IoU value as a float between 0.0 (no overlap) and 1.0 (perfect overlap).
    """
    x1, y1, w1, h1 = box_a
    x2, y2, w2, h2 = box_b

    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    inter_width = max(0, x_right - x_left)
    inter_height = max(0, y_bottom - y_top)
    inter_area = inter_width * inter_height

    if inter_area == 0:
        return 0.0

    box_a_area = w1 * h1
    box_b_area = w2 * h2
    union_area = box_a_area + box_b_area - inter_area

    return float(inter_area) / float(union_area)


def filter_detections(
    detections: List[Dict], iou_threshold: float = 0.5
) -> List[Dict]:
    """
    Filter overlapping detections using Non-Maximum Suppression (NMS).

    When two detections overlap (IoU > iou_threshold), keep the one with the
    larger area and discard the other.

    Args:
        detections: List of detection dictionaries (each must have 'bbox' and 'area').
        iou_threshold: IoU threshold above which two detections are considered overlapping.

    Returns:
        Filtered list of detections with overlapping duplicates removed.
    """
    sorted_dets = sorted(detections, key=lambda d: d['area'], reverse=True)
    kept_detections = []

    for det in sorted_dets:
        overlap = False
        for kept in kept_detections:
            if compute_iou(det['bbox'], kept['bbox']) > iou_threshold:
                overlap = True
                break
        if not overlap:
            kept_detections.append(det)

    return kept_detections
