import py_stuff.image_transform as it
import commands.send_wrapper as sw
import glob
import random
import os
import requests



man_description = str(
    "**$emoji Command**\n"
    "Usage: `$emoji <width> <pasted image>`\n"
    "Description: Generates emoji art of attached imaged (via paste or '+' button) of specified width. default width = 80. Max width on largest zoomout is 173\n"
)

async def run(message):

    default = 80
    contents = message.content
    args = contents.split(' ',1)
    if len(args) > 1:
        try:
            width = int(args[1].strip())
            if width > 173 or width < 0:
                await message.channel.send(f"Invalid input for 'width': {args[1]}. Using default = {default}")
                width = default
        except ValueError:
            await message.channel.send(f"Invalid input for 'width': {args[1]}. Using default = {default}")
            width = default
    else:
        width = default
    
    try:
        picture_url = str(message.attachments[0].url)
        page = requests.get(picture_url)
    except IndexError:
        await message.channel.send("No image attached")
        return

    f_ext = os.path.splitext(picture_url)[-1]
    f_name = 'img{}'.format(f_ext)
    f_name = f_name + ".png"
    with open(f_name, 'wb') as f:
        f.write(page.content)

    converted_image = it.resize_and_convert_image_with_custom_palette(f_name, width, it.emoji_palette)
    emoji_art = it.generate_emoji_art(converted_image, it.emoji_colors)
    os.remove(f"{f_name}")
    # print (emoji_art)
    await sw.wrapperSend(message, emoji_art,'mono')