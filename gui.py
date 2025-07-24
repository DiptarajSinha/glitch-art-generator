import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from glitch_effects import GlitchEffects
import os

class GlitchArtGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Free Glitch Art Generator")
        self.root.geometry("800x600")
        
        self.current_image = None
        self.original_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File operations frame
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="Reset", command=self.reset_image).pack(side=tk.LEFT)
        
        # Universal intensity slider
        intensity_frame = ttk.LabelFrame(main_frame, text="Effect Intensity")
        intensity_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(intensity_frame, text="Intensity:").grid(row=0, column=0, sticky='w', padx=5)
        
        # Variable shared by every effect
        self.intensity_var = tk.DoubleVar(value=0.3)
        
        intensity_slider = ttk.Scale(
            intensity_frame,
            from_=0.05,
            to=0.9,
            variable=self.intensity_var,
            orient='horizontal'
        )
        intensity_slider.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Display current value
        value_label = ttk.Label(intensity_frame, textvariable=self.intensity_var)
        value_label.grid(row=0, column=2, padx=5)
        
        intensity_frame.columnconfigure(1, weight=1)
        
        # Effects frame
        effects_frame = ttk.LabelFrame(main_frame, text="Glitch Effects")
        effects_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Effect buttons
        effects = [
            ("Pixel Sort", self.apply_pixel_sort),
            ("Channel Shift", self.apply_channel_shift),
            ("Random Noise", self.apply_noise),
            ("Data Corruption", self.apply_corruption),
            ("Scanline Effect", self.apply_scanline)
        ]
        
        for i, (name, command) in enumerate(effects):
            row, col = i // 3, i % 3
            ttk.Button(effects_frame, text=name, command=command).grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        for i in range(3):
            effects_frame.columnconfigure(i, weight=1)
        
        # Image display frame
        self.image_frame = ttk.LabelFrame(main_frame, text="Preview")
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_label = ttk.Label(self.image_frame, text="No image loaded")
        self.image_label.pack(expand=True)
    
    def get_params(self, effect_name, rate):
        """Map universal intensity to effect-specific parameters."""
        mapping = {
            "pixel_sort": {"threshold": rate},
            "random_noise": {"intensity": rate},
            "data_corruption": {"corruption_rate": rate * 0.15},
            "channel_shift": {"shift_amount": int(rate * 40)},
            "scanline": {"line_spacing": max(1, int((1 - rate) * 10))}
        }
        return mapping.get(effect_name, {})
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_image()
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
    
    def display_image(self):
        if self.current_image:
            # Resize for display
            display_size = (400, 300)
            display_image = self.current_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep reference
    
    def save_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        
        if file_path:
            try:
                self.current_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
    
    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image()
    
    def apply_effect(self, effect_function, **kwargs):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.current_image = effect_function(self.current_image, **kwargs)
            self.display_image()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply effect: {e}")
    
    def apply_pixel_sort(self):
        rate = self.intensity_var.get()
        params = self.get_params("pixel_sort", rate)
        self.apply_effect(GlitchEffects.pixel_sort, **params)
    
    def apply_channel_shift(self):
        rate = self.intensity_var.get()
        params = self.get_params("channel_shift", rate)
        self.apply_effect(GlitchEffects.channel_shift, **params)
    
    def apply_noise(self):
        rate = self.intensity_var.get()
        params = self.get_params("random_noise", rate)
        self.apply_effect(GlitchEffects.random_noise, **params)
    
    def apply_corruption(self):
        rate = self.intensity_var.get()
        params = self.get_params("data_corruption", rate)
        self.apply_effect(GlitchEffects.data_corruption, **params)
    
    def apply_scanline(self):
        rate = self.intensity_var.get()
        params = self.get_params("scanline", rate)
        self.apply_effect(GlitchEffects.scanline_effect, **params)
    
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = GlitchArtGUI()
    app.run()
