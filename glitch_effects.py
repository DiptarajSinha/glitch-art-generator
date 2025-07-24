import numpy as np
from PIL import Image
import random

class GlitchEffects:
    
    @staticmethod
    def pixel_sort(image, threshold=0.1):
        """Sort pixels based on brightness with threshold."""
        pixels = np.array(image)
        height, width = pixels.shape[:2]
        
        for row in pixels:
            # Create mask for sorting
            if len(row.shape) > 1:
                brightness = np.mean(row, axis=1)
                mask = brightness > threshold * 255
                sorted_pixels = row[mask]
                if len(sorted_pixels) > 0:
                    sorted_indices = np.argsort(np.mean(sorted_pixels, axis=1))
                    row[mask] = sorted_pixels[sorted_indices]
        
        return Image.fromarray(pixels)
    
    @staticmethod
    def channel_shift(image, shift_amount=10):
        """Shift RGB channels independently."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        r, g, b = image.split()
        
        # Convert to numpy for shifting
        r_array = np.array(r)
        g_array = np.array(g)
        b_array = np.array(b)
        
        # Shift channels
        r_shifted = np.roll(r_array, shift_amount, axis=1)
        g_shifted = np.roll(g_array, -shift_amount//2, axis=0)
        b_shifted = np.roll(b_array, shift_amount//3, axis=1)
        
        # Merge back
        shifted_image = Image.merge('RGB', (
            Image.fromarray(r_shifted),
            Image.fromarray(g_shifted),
            Image.fromarray(b_shifted)
        ))
        
        return shifted_image
    
    @staticmethod
    def random_noise(image, intensity=0.3):
        """Add random noise corruption with better visibility."""
        pixels = np.array(image)
        
        # Create more visible noise
        noise = np.random.randint(-intensity*255, intensity*255, pixels.shape)
        
        # Add noise and clamp values
        noisy_pixels = pixels.astype(np.int16) + noise.astype(np.int16)
        noisy_pixels = np.clip(noisy_pixels, 0, 255).astype(np.uint8)
        
        return Image.fromarray(noisy_pixels)
    
    @staticmethod
    def data_corruption(image, corruption_rate=0.05):
        """Simulate data corruption with more visible effects."""
        pixels = np.array(image)
        height, width = pixels.shape[:2]
        
        # Method 1: Random pixel corruption
        flat_pixels = pixels.flatten()
        num_corruptions = int(len(flat_pixels) * corruption_rate)
        corruption_indices = random.sample(range(len(flat_pixels)), num_corruptions)
        
        for idx in corruption_indices:
            flat_pixels[idx] = random.randint(0, 255)
        
        # Method 2: Add corrupted blocks for more dramatic effect
        for _ in range(random.randint(5, 15)):
            # Random block position and size
            block_x = random.randint(0, width - 20)
            block_y = random.randint(0, height - 20)
            block_w = random.randint(5, 20)
            block_h = random.randint(1, 5)
            
            # Fill block with random colors
            if block_y + block_h < height and block_x + block_w < width:
                corrupted_pixels = flat_pixels.reshape(pixels.shape)
                corrupted_pixels[block_y:block_y+block_h, block_x:block_x+block_w] = random.randint(0, 255)
        
        return Image.fromarray(flat_pixels.reshape(pixels.shape))
    
    @staticmethod
    def scanline_effect(image, line_spacing=3):
        """Create scanline interference effect."""
        pixels = np.array(image)
        height, width = pixels.shape[:2]
        
        # Add scanlines
        for i in range(0, height, line_spacing):
            if i < height:
                # Darken or brighten scanlines
                pixels[i] = pixels[i] * random.uniform(0.3, 1.5)
                pixels[i] = np.clip(pixels[i], 0, 255)
        
        return Image.fromarray(pixels.astype(np.uint8))
