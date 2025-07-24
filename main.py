from PIL import Image
import numpy as np
import random

def load_image(file_path):
    """Load and return an image."""
    return Image.open(file_path)

def save_image(image, output_path):
    """Save the processed image."""
    image.save(output_path)

def basic_pixel_sort(image):
    """Simple pixel sorting glitch effect."""
    # Convert to numpy array for manipulation
    pixels = np.array(image)
    height, width = pixels.shape[:2]
    
    # Sort pixels in random rows
    for i in range(0, height, random.randint(2, 10)):
        if i < height:
            # Sort by brightness
            row = pixels[i]
            brightness = np.mean(row, axis=1) if len(row.shape) > 1 else row
            sorted_indices = np.argsort(brightness)
            pixels[i] = row[sorted_indices]
    
    return Image.fromarray(pixels)

# Test the basic functionality
if __name__ == "__main__":
    # Load a test image
    img = load_image("generated-image.png")
    
    # Apply glitch effect
    glitched = basic_pixel_sort(img)
    
    # Save result
    save_image(glitched, "glitched_output.jpg")
    print("Glitch effect applied successfully!")
