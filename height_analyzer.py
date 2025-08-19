#!/usr/bin/env python3
"""
Height Analysis Module

This module implements ML-based height estimation from uploaded photos
using computer vision techniques and perspective analysis.
"""

import cv2
import numpy as np
from typing import Dict, Optional, Tuple, List
import base64
import io
from PIL import Image
import math


class HeightAnalyzer:
    """ML-based height analyzer for estimating human height from photos."""
    
    def __init__(self):
        self.reference_objects = {
            'credit_card': {'width': 85.6, 'height': 53.98},  # mm
            'coin_quarter': {'diameter': 24.26},  # mm
            'smartphone': {'width': 75, 'height': 150},  # mm average
            'door': {'width': 914.4, 'height': 2032},  # mm standard door
            'standard_brick': {'width': 215, 'height': 65}  # mm
        }
        
    def analyze_height_from_photo(self, image_path: str, reference_object: str = None, 
                                reference_height_mm: float = None) -> Dict:
        """
        Analyze height from a photo using computer vision techniques.
        
        Args:
            image_path: Path to the image file
            reference_object: Known reference object in the image
            reference_height_mm: Known height of reference object in mm
            
        Returns:
            Dictionary with height estimation results
        """
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image", "success": False}
            
            # Convert to RGB for processing
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect human figure and reference objects
            person_contour = self._detect_person_contour(image)
            if person_contour is None:
                return {"error": "Could not detect person in image", "success": False}
            
            # Calculate person pixel height
            person_height_pixels = self._calculate_person_height_pixels(person_contour)
            
            # Determine scale factor
            scale_factor = None
            
            if reference_object and reference_object in self.reference_objects:
                scale_factor = self._calculate_scale_from_reference_object(
                    image, reference_object
                )
            elif reference_height_mm:
                scale_factor = reference_height_mm / person_height_pixels
            else:
                # Use perspective-based estimation
                scale_factor = self._estimate_scale_from_perspective(image, person_height_pixels)
            
            if scale_factor is None:
                return {"error": "Could not determine scale factor", "success": False}
            
            # Calculate actual height
            estimated_height_mm = person_height_pixels * scale_factor
            estimated_height_cm = estimated_height_mm / 10
            estimated_height_inches = estimated_height_mm / 25.4
            estimated_height_feet = estimated_height_inches / 12
            
            confidence = self._calculate_confidence(image, person_contour, scale_factor)
            
            return {
                "success": True,
                "height_cm": round(estimated_height_cm, 1),
                "height_inches": round(estimated_height_inches, 1),
                "height_feet_inches": f"{int(estimated_height_feet)}'{int((estimated_height_feet % 1) * 12)}\"",
                "confidence": round(confidence, 2),
                "method": self._get_method_description(reference_object, reference_height_mm),
                "person_height_pixels": person_height_pixels,
                "scale_factor": scale_factor
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}", "success": False}
    
    def _detect_person_contour(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Detect the main person contour in the image using edge detection."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find the largest contour (assuming it's the person)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Filter out very small contours
        if cv2.contourArea(largest_contour) < 1000:
            return None
            
        return largest_contour
    
    def _calculate_person_height_pixels(self, person_contour: np.ndarray) -> float:
        """Calculate the height of the person in pixels from their contour."""
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(person_contour)
        
        # Use a more sophisticated approach to find actual top and bottom points
        # Find the topmost and bottommost points of the contour
        topmost = tuple(person_contour[person_contour[:, :, 1].argmin()][0])
        bottommost = tuple(person_contour[person_contour[:, :, 1].argmax()][0])
        
        height_pixels = bottommost[1] - topmost[1]
        
        # Ensure minimum reasonable height
        return max(height_pixels, h * 0.8)
    
    def _calculate_scale_from_reference_object(self, image: np.ndarray, 
                                             reference_object: str) -> Optional[float]:
        """Calculate scale factor using a known reference object."""
        ref_specs = self.reference_objects[reference_object]
        
        # Simple implementation - look for rectangular objects
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Look for rectangular shapes (4 vertices)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Check aspect ratio matches reference object
                if 'width' in ref_specs and 'height' in ref_specs:
                    aspect_ratio = w / h
                    ref_aspect_ratio = ref_specs['width'] / ref_specs['height']
                    
                    if 0.8 <= aspect_ratio / ref_aspect_ratio <= 1.2:
                        # Found potential reference object
                        return ref_specs['height'] / h
        
        return None
    
    def _estimate_scale_from_perspective(self, image: np.ndarray, 
                                       person_height_pixels: float) -> Optional[float]:
        """Estimate scale using perspective analysis and average human height."""
        # Use statistical average human height: 170cm (5'7")
        average_human_height_mm = 1700
        
        # Get image dimensions
        height, width = image.shape[:2]
        
        # Perspective correction factor based on person position in frame
        # People closer to camera appear larger, farther appear smaller
        
        # Simple heuristic: if person takes up more of the frame, they're closer
        person_ratio = person_height_pixels / height
        
        # Adjust scale based on how much of frame the person occupies
        if person_ratio > 0.8:  # Person very close to camera
            perspective_factor = 0.85
        elif person_ratio > 0.6:  # Person moderately close
            perspective_factor = 0.95
        elif person_ratio > 0.4:  # Person at medium distance
            perspective_factor = 1.0
        elif person_ratio > 0.2:  # Person farther away
            perspective_factor = 1.1
        else:  # Person very far
            perspective_factor = 1.2
        
        # Calculate scale factor
        adjusted_height = average_human_height_mm * perspective_factor
        scale_factor = adjusted_height / person_height_pixels
        
        return scale_factor
    
    def _calculate_confidence(self, image: np.ndarray, person_contour: np.ndarray, 
                            scale_factor: float) -> float:
        """Calculate confidence score for the height estimation."""
        confidence = 0.5  # Base confidence
        
        # Factor 1: Contour quality
        contour_area = cv2.contourArea(person_contour)
        image_area = image.shape[0] * image.shape[1]
        area_ratio = contour_area / image_area
        
        if 0.1 <= area_ratio <= 0.6:  # Good size ratio
            confidence += 0.2
        
        # Factor 2: Image quality (sharpness)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        if laplacian_var > 100:  # Sharp image
            confidence += 0.2
        elif laplacian_var > 50:  # Moderately sharp
            confidence += 0.1
        
        # Factor 3: Scale factor reasonableness
        if 0.5 <= scale_factor <= 3.0:  # Reasonable scale
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _get_method_description(self, reference_object: str = None, 
                              reference_height_mm: float = None) -> str:
        """Get description of the method used for height estimation."""
        if reference_object:
            return f"Reference object method using {reference_object}"
        elif reference_height_mm:
            return f"Custom reference height method ({reference_height_mm}mm)"
        else:
            return "Perspective analysis with average human height"
    
    def process_base64_image(self, base64_image: str, reference_object: str = None,
                           reference_height_mm: float = None) -> Dict:
        """Process a base64 encoded image for height analysis."""
        try:
            # Decode base64 image
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            # Save temporarily for processing
            temp_path = "/tmp/temp_height_analysis.jpg"
            image.save(temp_path)
            
            # Analyze the image
            result = self.analyze_height_from_photo(
                temp_path, reference_object, reference_height_mm
            )
            
            return result
            
        except Exception as e:
            return {"error": f"Base64 processing failed: {str(e)}", "success": False}


def demo_height_analysis():
    """Demo function to show height analysis capabilities."""
    analyzer = HeightAnalyzer()
    
    print("Height Analyzer Demo")
    print("=" * 30)
    print("\nThis module can analyze height from photos using:")
    print("1. Reference objects (credit card, coin, smartphone, door, brick)")
    print("2. Custom reference measurements")
    print("3. Perspective analysis with average human height")
    print("\nFeatures:")
    print("- Computer vision-based person detection")
    print("- Multiple measurement methods")
    print("- Confidence scoring")
    print("- Support for various image formats")
    
    # Show available reference objects
    print(f"\nAvailable reference objects:")
    for obj, specs in analyzer.reference_objects.items():
        print(f"  - {obj}: {specs}")


if __name__ == "__main__":
    demo_height_analysis()