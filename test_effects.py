from PIL import Image
from glitch_effects import GlitchEffects

def test_all_effects(input_image_path):
    """Test all glitch effects on an image."""
    original = Image.open(input_image_path)
    
    effects = {
        'pixel_sort': GlitchEffects.pixel_sort,
        'channel_shift': GlitchEffects.channel_shift,
        'random_noise': GlitchEffects.random_noise,
        'data_corruption': GlitchEffects.data_corruption,
        'scanline_effect': GlitchEffects.scanline_effect
    }
    
    for effect_name, effect_function in effects.items():
        try:
            result = effect_function(original)
            result.save(f"output_{effect_name}.jpg")
            print(f"✓ {effect_name} applied successfully")
        except Exception as e:
            print(f"✗ {effect_name} failed: {e}")

if __name__ == "__main__":
    test_all_effects("your_image_name.jpg")  # Change to your actual image filename
