#!/usr/bin/env python3
"""
Test script for height analysis functionality
"""

import sys
import numpy as np
import cv2
from height_analyzer import HeightAnalyzer


def create_test_image():
    """Create a simple test image with a person-like shape for testing."""
    # Create a blank image
    img = np.zeros((600, 400, 3), dtype=np.uint8)
    img.fill(255)  # White background
    
    # Draw a simple person-like figure
    # Head (circle)
    cv2.circle(img, (200, 100), 30, (0, 0, 0), 2)
    
    # Body (rectangle)
    cv2.rectangle(img, (170, 130), (230, 350), (0, 0, 0), 2)
    
    # Arms
    cv2.line(img, (170, 180), (120, 220), (0, 0, 0), 2)
    cv2.line(img, (230, 180), (280, 220), (0, 0, 0), 2)
    
    # Legs
    cv2.line(img, (185, 350), (150, 450), (0, 0, 0), 2)
    cv2.line(img, (215, 350), (250, 450), (0, 0, 0), 2)
    
    # Add a reference object (smartphone-like rectangle)
    cv2.rectangle(img, (320, 200), (350, 280), (100, 100, 100), -1)
    cv2.putText(img, "Phone", (325, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return img


def test_height_analyzer():
    """Test the height analyzer with a synthetic image."""
    print("Testing Height Analyzer")
    print("=" * 30)
    
    # Create test image
    test_img = create_test_image()
    test_path = "/tmp/test_person.jpg"
    cv2.imwrite(test_path, test_img)
    
    print(f"Created test image: {test_path}")
    
    # Initialize analyzer
    analyzer = HeightAnalyzer()
    
    # Test 1: Basic analysis without reference
    print("\nTest 1: Basic perspective analysis")
    result1 = analyzer.analyze_height_from_photo(test_path)
    print(f"Result: {result1}")
    
    # Test 2: With smartphone reference
    print("\nTest 2: With smartphone reference")
    result2 = analyzer.analyze_height_from_photo(test_path, reference_object="smartphone")
    print(f"Result: {result2}")
    
    # Test 3: With custom reference height
    print("\nTest 3: With custom reference height")
    result3 = analyzer.analyze_height_from_photo(test_path, reference_height_mm=150)
    print(f"Result: {result3}")
    
    # Test 4: Error handling - non-existent file
    print("\nTest 4: Error handling")
    result4 = analyzer.analyze_height_from_photo("/nonexistent/file.jpg")
    print(f"Result: {result4}")


def test_cli_integration():
    """Test CLI integration."""
    print("\nTesting CLI Integration")
    print("=" * 30)
    
    # Import the CLI function
    from cli import analyze_height_from_photo
    
    # Create test image
    test_img = create_test_image()
    test_path = "/tmp/test_person_cli.jpg"
    cv2.imwrite(test_path, test_img)
    
    print("Running CLI height analysis:")
    analyze_height_from_photo(test_path, reference_object="smartphone")


if __name__ == "__main__":
    print("Height Analysis Test Suite")
    print("=" * 40)
    
    try:
        test_height_analyzer()
        test_cli_integration()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)