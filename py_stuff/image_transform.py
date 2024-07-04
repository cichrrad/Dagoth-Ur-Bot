from PIL import Image

# Define the custom ANSI palette (using the colors you specified)
ansi_palette = [
    79, 84, 92,   # Dark gray
    220, 50, 47,  # Red
    133, 153, 0,  # Olive
    181, 137, 0,  # Gold
    38, 139, 210, # Blue
    211, 54, 130, # Pink
    42, 161, 152, # Teal
    255, 255, 255 # White
] + [0] * (256 * 3 - 24)  # Fill the rest of the palette with zeros

# Define the custom emoji palette (using the colors you specified)
emoji_palette = [
    244, 67, 54,  # Red
    255, 152, 0,  # Orange
    255, 204, 50, # Yellow
    124, 179, 66, # Green
    25, 118, 210, # Blue
    171, 71, 188, # Purple
    183, 109, 84, # Brown
    66, 66, 66,   # Gray
    224, 224, 224 # Light gray / white
] + [0] * (256 * 3 - 27)  # Fill the rest of the palette with zeros

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

# Emoji representations for the colors
emoji_colors = [
    "🟥",  # Red
    "🟧",  # Orange
    "🟨",  # Yellow
    "🟩",  # Green
    "🟦",  # Blue
    "🟪",  # Purple
    "🟫",  # Brown
    "⬛",  # Gray
    "⬜"   # Light gray / white
]

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

def generate_emoji_art(image, emoji_colors):
    emoji_art = ""
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            color_index = pixels[x, y]
            if color_index < len(emoji_colors):
                emoji_art += emoji_colors[color_index]
            else:
                emoji_art += "⬛"
        emoji_art += "\n"
    
    return emoji_art

