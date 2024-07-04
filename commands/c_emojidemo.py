import py_stuff.image_transform as it
import commands.send_wrapper as sw
import glob
import random


man_description = str(
    "Demo showcase of color emoji output. Work in progress.\n"
)

async def run(message):

    await message.channel.send("\n WORK IN PROGRESS.\nMax 'width' = 173 emojis with max zoomout.\nFor larger resolutions, 'pixel rows' will overflow.")

    input_image_path = random.choice(glob.glob('./py_stuff/*.png'))
    target_width = 173 # Set target width for the art (MAX IS 173 - on max zoomout this is the largest resolution without row overflow)

    converted_image = it.resize_and_convert_image_with_custom_palette(input_image_path, target_width, it.emoji_palette)
    emoji_art = it.generate_emoji_art(converted_image, it.emoji_colors)
    #print (emoji_art)
    await sw.wrapperSend(message, emoji_art,'mono')