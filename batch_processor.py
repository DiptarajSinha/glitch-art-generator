import os
from PIL import Image
from glitch_effects import GlitchEffects

def batch_process_folder(input_folder, output_folder, effect_name='pixel_sort'):
    """Process all images in a folder with specified effect."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    effects_map = {
        'pixel_sort': GlitchEffects.pixel_sort,
        'channel_shift': GlitchEffects.channel_shift,
        'random_noise': GlitchEffects.random_noise,
        'data_corruption': GlitchEffects.data_corruption,
        'scanline_effect': GlitchEffects.scanline_effect
    }
    
    effect_function = effects_map.get(effect_name, GlitchEffects.pixel_sort)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"glitched_{filename}")
            
            try:
                image = Image.open(input_path)
                glitched = effect_function(image)
                glitched.save(output_path)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    batch_process_folder("input_images", "output_images", "pixel_sort")
