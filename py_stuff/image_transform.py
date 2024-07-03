from PIL import Image

# Define the custom palette (using the colors you specified)
custom_palette = [
    79, 84, 92,   # Dark gray
    220, 50, 47,  # Red
    133, 153, 0,  # Olive
    181, 137, 0,  # Gold
    38, 139, 210, # Blue
    211, 54, 130, # Pink
    42, 161, 152, # Teal
    255, 255, 255 # White
] + [0] * (256 * 3 - 24)  # Fill the rest of the palette with zeros

# ANSI escape codes for Discord
ansi_colors = [
    "\u001b[0;30m",  # Dark gray
    "\u001b[0;31m",  # Red
    "\u001b[0;32m",  # Olive
    "\u001b[0;33m",  # Gold
    "\u001b[0;34m",  # Blue
    "\u001b[0;35m",  # Pink
    "\u001b[0;36m",  # Teal
    "\u001b[0;37m",  # White
]
ansi_reset = "\u001b[0;0m"

def resize_and_convert_image_with_custom_palette(input_path, target_width, palette):
    with Image.open(input_path) as img:
        original_width, original_height = img.size
        if original_width > target_width:
            aspect_ratio = original_height / original_width
            new_height = int(target_width * aspect_ratio)
            img = img.resize((target_width, new_height), Image.RASTERIZE)
        
        # Convert image to RGB
        img = img.convert("RGB")
        
        # Create a palette image
        palette_img = Image.new("P", (1, 1))
        palette_img.putpalette(palette)

        # Convert the image to use the palette
        img = img.quantize(palette=palette_img)
        
        return img

def generate_ascii_art(image, palette, ansi_colors, ansi_reset):
    ascii_art = ""
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        current_color = None
        for x in range(width):
            color_index = pixels[x, y]
            if color_index < len(ansi_colors):
                if color_index != current_color:
                    if current_color is not None:
                        ascii_art += ansi_reset
                    ascii_art += ansi_colors[color_index]
                    current_color = color_index
                ascii_art += "■"
            else:
                ascii_art += " "
        ascii_art += ansi_reset + "\n"  # Ensure each row ends with a reset code
    
    return ascii_art

# Example usage
# input_image_path = '/home/rdk/Projects/Dagoth-Ur-Bot/py_stuff/mario-hero.png'
# target_width = 111  # Set target width for the ASCII art

# converted_image = resize_and_convert_image_with_custom_palette(input_image_path, target_width, custom_palette)
# ascii_art = generate_ascii_art(converted_image, custom_palette, ansi_colors, ansi_reset)

# # Print or save the ASCII art
# output_ascii_path = '/home/rdk/Projects/Dagoth-Ur-Bot/py_stuff/ascii_art.txt'
# with open(output_ascii_path, 'w') as f:
#     f.write(ascii_art)

# print("ASCII art generated and saved to:", output_ascii_path)
