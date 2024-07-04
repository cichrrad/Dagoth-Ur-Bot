# TODO FIGURE OUT DISCORD ANSI BS TO ALLOW FOR COLOR ASCII ART

import os
import urllib.request
from ascii_magic import AsciiArt
import requests
import commands.send_wrapper as sw

man_description = str(
    "**$ascii Command**\n"
    "Usage: `$ascii <width> <pasted picture>`\n"
    "Description: Generates ASCII art of attached imaged (via paste or '+' button) of specified width. default width = 111. Should you have problems with image rows overflow, try a smaller width or larger zoom out. Max width on largest zoomout is ~350\n"
    "Example:\n"
    "```\n"
    "$asci 200 * + picture *\n"
    "```\n"
    "The bot will respond with the ASCII art of the image of width 200."

)

async def run(message):
    default = 111
    contents = message.content
    args = contents.split(' ',1)
    if len(args) > 1:
        try:
            width = int(args[1].strip())
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
    my_art = AsciiArt.from_image(f_name)
    os.remove(f"{f_name}")
    asc = my_art.to_ascii(columns=width, monochrome= True)
    await sw.wrapperSend(message,(str(asc)).replace('`','ˋ'),'mono')