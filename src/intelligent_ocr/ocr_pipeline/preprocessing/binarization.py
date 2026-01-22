"""Image binarization (thresholding) for OCR preprocessing."""

import cv2
import numpy as np


def binarize_otsu(image: np.ndarray) -> np.ndarray:
    """
    Binarize image using Otsu's thresholding method.
    
    Automatically determines optimal threshold value.
    Best for images with bimodal histogram.
    
    Args:
        image: Input grayscale image
        
    Returns:
        Binary image (0 or 255)
    """
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def binarize_adaptive(image: np.ndarray, method: str = "gaussian", block_size: int = 11, C: int = 2) -> np.ndarray:
    """
    Binarize image using adaptive thresholding.
    
    Better for images with varying lighting conditions.
    
    Args:
        image: Input grayscale image
        method: Adaptive method ("gaussian" or "mean")
        block_size: Size of neighborhood area (must be odd)
        C: Constant subtracted from mean
        
    Returns:
        Binary image (0 or 255)
    """
    if block_size % 2 == 0:
        block_size += 1
    
    if method == "gaussian":
        adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    else:
        adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
    
    binary = cv2.adaptiveThreshold(
        image,
        255,
        adaptive_method,
        cv2.THRESH_BINARY,
        block_size,
        C
    )
    
    return binary


def binarize_sauvola(image: np.ndarray, window_size: int = 15, k: float = 0.2) -> np.ndarray:
    """
    Binarize image using Sauvola's method (local thresholding).
    
    Implementation of Sauvola's algorithm for document binarization.
    
    Args:
        image: Input grayscale image
        window_size: Size of local window (must be odd)
        k: Parameter controlling threshold (typically 0.2-0.5)
        
    Returns:
        Binary image (0 or 255)
    """
    if window_size % 2 == 0:
        window_size += 1
    
    # Convert to float for calculations
    img_float = image.astype(np.float32)
    
    # Calculate local mean using box filter
    mean = cv2.boxFilter(img_float, cv2.CV_32F, (window_size, window_size))
    
    # Calculate local standard deviation
    mean_sq = cv2.boxFilter(img_float ** 2, cv2.CV_32F, (window_size, window_size))
    std = np.sqrt(mean_sq - mean ** 2)
    
    # Calculate threshold
    threshold = mean * (1 + k * ((std / 128) - 1))
    
    # Apply threshold
    binary = (img_float > threshold).astype(np.uint8) * 255
    
    return binary


def binarize_simple(image: np.ndarray, threshold_value: int = 127) -> np.ndarray:
    """
    Simple binary thresholding with fixed threshold value.
    
    Args:
        image: Input grayscale image
        threshold_value: Threshold value (0-255)
        
    Returns:
        Binary image (0 or 255)
    """
    _, binary = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary


def binarize_image(
    image: np.ndarray,
    method: str = "otsu",
    **kwargs
) -> np.ndarray:
    """
    Binarize image using specified method.
    
    Args:
        image: Input grayscale image
        method: Binarization method ("otsu", "adaptive", "sauvola", or "simple")
        **kwargs: Additional parameters for specific methods
        
    Returns:
        Binary image (0 or 255)
    """
    if method == "otsu":
        return binarize_otsu(image)
    elif method == "adaptive":
        block_size = kwargs.get("block_size", 11)
        C = kwargs.get("C", 2)
        adaptive_method = kwargs.get("adaptive_method", "gaussian")
        return binarize_adaptive(image, method=adaptive_method, block_size=block_size, C=C)
    elif method == "sauvola":
        window_size = kwargs.get("window_size", 15)
        k = kwargs.get("k", 0.2)
        return binarize_sauvola(image, window_size=window_size, k=k)
    elif method == "simple":
        threshold_value = kwargs.get("threshold_value", 127)
        return binarize_simple(image, threshold_value=threshold_value)
    else:
        # Default to Otsu
        return binarize_otsu(image)
