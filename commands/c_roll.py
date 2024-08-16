import random

import py_stuff.send_wrapper as sw

man_description = str(
    "**$roll Command**\n"
    "Usage: `$roll <min> <max>`\n"
    "Description: Rolls a random number between <min> and <max>. If <min> and <max> are not specified, defaults to 1 and 6 respectively. If only one argument is specified, it is taken as <max>.\n"
    "Example:\n"
    "```\n"
    "$roll 1 6\n"
    "```\n"
    "This command will roll a random number between 1 and 6."
)


async def run(message):
    contents = message.content
    args = contents.split(' ', 1)
    default_min = 1
    default_max = 6
    if len(args) > 1:
        #see if both min and max are specified
        if ' ' in args[1]:
            try:
                min = int(args[1].split(' ')[0].strip())
                max = int(args[1].split(' ')[1].strip())
            except ValueError:
                min = default_min
                max = default_max
                await message.channel.send(f"Invalid input for 'min' or 'max' Using defaults of {default_min} and {default_max}.")
        else:
            min = default_min
            #assume the max is specified
            try:
                max = int(args[1].strip())
            except ValueError:
                max = default_max
                await message.channel.send(f"Invalid input for 'max' Using default of {default_max}.")
    else:
        #if nothing is specified
        min = default_min
        max = default_max

    roll = random.randint(min, max)
    await sw.wrapperSend(message, f"You rolled {roll}!", 'mono')