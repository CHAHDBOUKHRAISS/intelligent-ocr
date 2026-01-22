"""Image preprocessing pipeline for OCR optimization."""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any

from intelligent_ocr.ocr_pipeline.preprocessing.normalization import (
    convert_to_grayscale,
    deskew_image,
    normalize_image,
    enhance_contrast as enhance_contrast_func
)
from intelligent_ocr.ocr_pipeline.preprocessing.denoising import (
    clean_image,
    remove_noise_bilateral
)
from intelligent_ocr.ocr_pipeline.preprocessing.binarization import (
    binarize_image,
    binarize_otsu
)


def preprocess_image(
    image: np.ndarray,
    deskew: bool = True,
    denoise: bool = True,
    binarize: bool = True,
    denoise_method: str = "bilateral",
    binarize_method: str = "otsu",
    enhance_contrast: bool = True
) -> Dict[str, Any]:
    """
    Complete preprocessing pipeline for OCR optimization.
    
    Steps:
    1. Convert to grayscale
    2. Enhance contrast (optional)
    3. Deskew image (optional)
    4. Remove noise (optional)
    5. Binarize image (optional)
    
    Args:
        image: Input image (BGR, RGB, or grayscale)
        deskew: Whether to deskew the image
        denoise: Whether to remove noise
        binarize: Whether to binarize the image
        denoise_method: Denoising method ("bilateral", "gaussian", "median")
        binarize_method: Binarization method ("otsu", "adaptive", "sauvola")
        enhance_contrast: Whether to enhance contrast
        
    Returns:
        Dictionary containing:
            - processed_image: Preprocessed image
            - skew_angle: Detected skew angle (if deskewed)
            - steps_applied: List of preprocessing steps applied
    """
    steps_applied = []
    skew_angle = 0.0
    
    if len(image.shape) == 3:
        processed = convert_to_grayscale(image)
        steps_applied.append("grayscale")
    else:
        processed = image.copy()
    
    if enhance_contrast:
        processed = enhance_contrast_func(processed)
        steps_applied.append("contrast_enhancement")
    
    if deskew:
        processed, skew_angle = deskew_image(processed)
        if abs(skew_angle) > 0.1:
            steps_applied.append(f"deskew_{skew_angle:.2f}deg")
    
    if denoise:
        processed = clean_image(processed, method=denoise_method)
        steps_applied.append(f"denoise_{denoise_method}")
    
    if binarize:
        processed = binarize_image(processed, method=binarize_method)
        steps_applied.append(f"binarize_{binarize_method}")
    
    return {
        "processed_image": processed,
        "skew_angle": skew_angle,
        "steps_applied": steps_applied
    }


def preprocess_from_file(
    file_path: Path,
    deskew: bool = True,
    denoise: bool = True,
    binarize: bool = True,
    denoise_method: str = "bilateral",
    binarize_method: str = "otsu",
    enhance_contrast: bool = True
) -> Dict[str, Any]:
    """
    Load image from file and preprocess it.
    
    Args:
        file_path: Path to image file
        deskew: Whether to deskew the image
        denoise: Whether to remove noise
        binarize: Whether to binarize the image
        denoise_method: Denoising method
        binarize_method: Binarization method
        enhance_contrast: Whether to enhance contrast
        
    Returns:
        Dictionary containing preprocessing results
    """

    image = cv2.imread(str(file_path))
    
    if image is None:
        raise ValueError(f"Could not load image from {file_path}")
    
    
    return preprocess_image(
        image,
        deskew=deskew,
        denoise=denoise,
        binarize=binarize,
        denoise_method=denoise_method,
        binarize_method=binarize_method,
        enhance_contrast=enhance_contrast
    )
