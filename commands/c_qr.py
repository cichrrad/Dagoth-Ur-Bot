import discord
import qrcode
import os
import commands.send_wrapper as sw

man_description = str(
    "**$qr Command**\n"
    "Usage: `$qr <text>`\n"
    "Description: Sends a QR code for the specified text.\n"
    "Example:\n"
    "```\n"
    "$qr hello world\n"
    "```\n"
    "The bot will respond with a QR code for the specified text."
)

async def run(message):
    default = "Come Nerevar, friend or traitor, come. Come and look upon the Heart and Akulakahn, and bring Wraithguard, I have need of it. Come to the Heart chamber, I wait for you there, where we last met, countless ages ago. Come to me through fire and war, I welcome you! Welcome Moon-and-Star, I have prepared a place for you! Come, bring Wraithguard to the Heart chamber, together, let us free the cursed false gods! Welcome Nerevar, together we shall speak for the law and the land and drive the mongrel dogs of the Empire from Morrowind! Is this how you honor the 6th house and the tribe unmourned? Come to me openly, and not by stealth. Dagoth Ur welcomes you Nerevar, my old friend... but to this place where destiny is made, why have you come unprepared? Welcome, Moon-and-Star, to this place where YOUR destiny is made. What a fool you are, I'm a god! How can you kill a god? What a grand and intoxicating innocence! How could you be so naive? There is no escape, no recall or intervention can work in this place! Come! Lay down your weapons! It is not too late for my mercy... "
    if len(message.content.split(' ',1)) > 1:
        text = (message.content.split(' ',1))[1].strip()
    else:
        text = default
    
    qr = qrcode.QRCode()
    qr.add_data(str(text))
    img = qr.make_image()
    img.save('qr.png')
    await message.channel.send(file=discord.File('qr.png'))
    os.remove('qr.png')