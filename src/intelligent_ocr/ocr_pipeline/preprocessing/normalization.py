"""Image normalization and deskewing for OCR preprocessing."""

import cv2
import numpy as np
from typing import Tuple, Optional


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert image to grayscale.
    
    Args:
        image: Input image (BGR or RGB)
        
    Returns:
        Grayscale image
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def detect_skew_angle(image: np.ndarray) -> float:
    """
    Detect skew angle of document image.
    
    Uses Hough Line Transform to detect lines and calculate average angle.
    
    Args:
        image: Grayscale image
        
    Returns:
        Skew angle in degrees
    """
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    if lines is None or len(lines) == 0:
        return 0.0
    
    angles = []
    for line in lines:
        rho, theta = line[0]
        angle = np.degrees(theta) - 90
        if angle < -45:
            angle += 90
        elif angle > 45:
            angle -= 90
        angles.append(angle)
    return np.median(angles) if angles else 0.0


def deskew_image(image: np.ndarray, angle: Optional[float] = None) -> Tuple[np.ndarray, float]:
    """
    Deskew image by rotating it to correct orientation.
    
    Args:
        image: Input grayscale image
        angle: Skew angle in degrees (if None, will be detected automatically)
        
    Returns:
        Tuple of (deskewed_image, detected_angle)
    """
    if angle is None:
        angle = detect_skew_angle(image)
    
    if abs(angle) < 0.1:
        return image, angle
    
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]
    
    deskewed = cv2.warpAffine(
        image,
        rotation_matrix,
        (new_w, new_h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    
    return deskewed, angle


def enhance_contrast(image: np.ndarray, alpha: float = 1.2, beta: int = 10) -> np.ndarray:
    """
    Enhance image contrast using linear transformation.
    
    Args:
        image: Input grayscale image
        alpha: Contrast control (1.0 = no change, >1.0 = more contrast)
        beta: Brightness control (0 = no change)
        
    Returns:
        Contrast-enhanced image
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def normalize_image(image: np.ndarray, enhance: bool = True) -> np.ndarray:
    """
    Normalize image: convert to grayscale and optionally enhance contrast.
    
    Args:
        image: Input image (BGR, RGB, or grayscale)
        enhance: Whether to enhance contrast
        
    Returns:
        Normalized grayscale image
    """
    gray = convert_to_grayscale(image)
    
    if enhance:
        gray = enhance_contrast(gray)
    
    return gray
