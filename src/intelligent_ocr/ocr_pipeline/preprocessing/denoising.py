"""Noise removal and image cleaning for OCR preprocessing."""

import cv2
import numpy as np


def remove_noise_gaussian(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Remove noise using Gaussian blur.
    
    Args:
        image: Input grayscale image
        kernel_size: Size of Gaussian kernel (must be odd)
        
    Returns:
        Denoised image
    """
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def remove_noise_bilateral(image: np.ndarray, d: int = 9, sigma_color: int = 75, sigma_space: int = 75) -> np.ndarray:
    """
    Remove noise using bilateral filter (preserves edges).
    
    Args:
        image: Input grayscale image
        d: Diameter of pixel neighborhood
        sigma_color: Filter sigma in color space
        sigma_space: Filter sigma in coordinate space
        
    Returns:
        Denoised image
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def remove_noise_morphological(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Remove noise using morphological operations.
    
    Useful for removing small noise particles.
    
    Args:
        image: Input binary image
        kernel_size: Size of morphological kernel
        
    Returns:
        Denoised image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    denoised = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    
    return denoised


def remove_salt_pepper_noise(image: np.ndarray, method: str = "median") -> np.ndarray:
    """
    Remove salt-and-pepper noise.
    
    Args:
        image: Input grayscale image
        method: Denoising method ("median" or "bilateral")
        
    Returns:
        Denoised image
    """
    if method == "median":
        return cv2.medianBlur(image, 5)
    elif method == "bilateral":
        return remove_noise_bilateral(image)
    else:
        return image


def clean_image(image: np.ndarray, method: str = "bilateral") -> np.ndarray:
    """
    Clean image by removing noise.
    
    Args:
        image: Input grayscale image
        method: Denoising method ("gaussian", "bilateral", "median", or "morphological")
        
    Returns:
        Cleaned image
    """
    if method == "gaussian":
        return remove_noise_gaussian(image)
    elif method == "bilateral":
        return remove_noise_bilateral(image)
    elif method == "median":
        return remove_salt_pepper_noise(image, method="median")
    elif method == "morphological":
        return remove_noise_morphological(image)
    else:
        return image
