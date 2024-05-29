from email.message import Message
from multiprocessing.connection import Client
from site import ENABLE_USER_SITE
from tokenize import Double
from xml.etree.ElementTree import tostring
import discord
import requests
import pyfiglet
import io
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import numexpr as ne
from translate import Translator
import shlex 
import random
import pandas as pd
import grammar


# Core function
async def callCommand(message, prefix):
    # REGISTER COMMANDS HERE
    commandList = [
        f"{prefix}ping", f"{prefix}plot", f"{prefix}man", f"{prefix}commands",
        f"{prefix}translate", f"{prefix}sort", f"{prefix}roll", f"{prefix}morrowgen"
    ]
    
    # PARSING COMMANDS HERE
    message_raw = (message.content).strip()
    args = shlex.split(message_raw)
    print(args)

    # IDENTIFY COMMANDS HERE
    if args[0] in commandList:
        await execute(args[0], args, message, prefix, commandList)
        return
    
    # Failed to identify
    await message.channel.send(f'I dont recognize \"' + str(args[0]) + '\" as a command.')
    return

# Separate command functions
async def command_ping(args, message):
    await message.channel.send('**Pong!**')

async def command_plot(args, message, commandList):
    # Defaults
    x_start = -10
    x_end = 10
    points = 100
    x_label = 'x'
    y_label = 'f(x)'
    x_ticks = 'auto'
    y_ticks = 'auto'
    title = 'Plot'
    x = np.linspace(int(x_start), int(x_end), int(points))
    func = x
    show_grid = True
    
    # Parsing user args
    keyed_args = {item.split('=')[0]: item.split('=')[1] for item in args[1:len(args)]}
    print(f"Parsed arguments are: {keyed_args}")
    
    # Validate and set 'from' (x_start)
    if 'from' in keyed_args:
        try:
            x_start = float(keyed_args['from'])
        except ValueError:
            await message.channel.send(f"Invalid input for 'from': {keyed_args['from']}. Using default = {x_start}")

    # Validate and set 'to' (x_end)
    if 'to' in keyed_args:
        try:
            x_end = float(keyed_args['to'])
        except ValueError:
            await message.channel.send(f"Invalid input for 'to': {keyed_args['to']}. Using default = {x_end}")

    # Validate and set 'points'
    if 'points' in keyed_args:
        try:
            points = int(keyed_args['points'])
            if points <= 0:
                raise ValueError("Points must be a positive integer")
        except ValueError:
            await message.channel.send(f"Invalid input for 'points': {keyed_args['points']}. Using default = {points}")

    if 'xTicks' in keyed_args:
        try:
            x_ticks = int(keyed_args['xTicks'])
            if x_ticks <= 0:
                raise ValueError("xTicks must be a positive integer")
        except ValueError:
            await message.channel.send(f"Invalid input for 'xTicks': {keyed_args['xTicks']}. Using default xTicks={x_ticks}")

    if 'yTicks' in keyed_args:
        try:
            y_ticks = int(keyed_args['yTicks'])
            if y_ticks <= 0:
                raise ValueError("yTicks must be a positive integer")
        except ValueError:
            await message.channel.send(f"Invalid input for 'yTicks': {keyed_args['yTicks']}. Using default yTicks={y_ticks}")

    if 'grid' in keyed_args:
        show_grid = keyed_args['grid'].lower() == 'true'

    if 'title' in keyed_args:
        title = keyed_args['title']

    if 'function' in keyed_args:
        expression = keyed_args['function']
        try:
            x = np.linspace(int(x_start), int(x_end), int(points))
            func = ne.evaluate(expression, local_dict={'x': x})
        except Exception as e:
            await message.channel.send(f"Failed to evaluate function '{expression}': {e}")
            func = x

    # Plot
    x = np.linspace(int(x_start), int(x_end), int(points))
    plt.figure()
    plt.plot(x, func)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if x_ticks != 'auto':
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=x_ticks))
    if y_ticks != 'auto':
        plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=y_ticks))
    if show_grid:
        plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Rewind the buffer to the beginning so it can be read
    plt.close()  # Close the figure to free up memory
    await message.channel.send(file=discord.File(buf, 'plot.png'))

async def command_translate(args, message,commandList):
    keyed_args = {item.split('=')[0]: item.split('=')[1] for item in args[1:len(args)]}
    print(f"Parsed arguments are: {keyed_args}")
    from_lang = 'none'
    to_lang = 'none'
    text = 'none'

    if 'from' in keyed_args:
        from_lang = keyed_args['from']
    if 'to' in keyed_args:
        to_lang = keyed_args['to']
    if 'text' in keyed_args:
        text = keyed_args['text']

    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(text)
    if 'INVALID SOURCE LANGUAGE' in translation:
        translation = f"Bad language code. See ```https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes```"
        await message.channel.send(f'{translation} (set 1) column.')
        return
    await message.channel.send(f'Translated Text: {translation}')

async def command_sort(args, message,commandList):
    keyed_args = {item.split('=')[0]: item.split('=')[1] for item in args[1:len(args)]}
    
    mode = 'up'
    if 'mode' in keyed_args:
        mode = keyed_args['mode']

    if 'data' in keyed_args:
        data = keyed_args['data'].split(',')
        if mode == 'up':
            data.sort()
        elif mode == 'down':
            data.sort(reverse=True)
        else:
            await message.channel.send(f"unknown mode \"{mode}\"")
            return 
    await message.channel.send(f"```{data}```")

async def command_roll(args, message,commandList):
    keyed_args = {item.split('=')[0]: item.split('=')[1] for item in args[1:len(args)]}
    sides = 6
    count = 1

    if 'sides' in keyed_args:
        try:
            parsedSides = int(keyed_args['sides'])
            if parsedSides <= 0:
                raise ValueError(f"Cannot roll a non-positive sided die (duh). Using default = {sides}")
            else:
                sides = parsedSides
        except ValueError:
            await message.channel.send(f"Invalid input for 'sides': {keyed_args['sides']}. Using default = {sides}")
    
    if 'count' in keyed_args:
        try:
            parsedCount = int(keyed_args['count'])
            if parsedCount <= 0:
                raise ValueError(f"Cannot roll a non-positive number of dice (duh). Using default = {count}")
            else:
                count = parsedCount
        except ValueError:
            await message.channel.send(f"Invalid input for 'count': {keyed_args['count']}. Using default = {count}")

    rolls = ""
    _sum = 0
    for roll in range(0, count, 1):
        rolled = random.randint(1, sides)
        _sum = _sum + rolled
        rolls = rolls + f"[{str(rolled)}]\n"
    avg = _sum / count
    avg = round(avg, 4)
    await message.channel.send(f"```\n{rolls}==========================\nAverage value = {str(avg)}\n==========================```")

async def command_morrowgen(args, message,commandList):
    race_list = ["Argonian", "Breton", "Dunmer", "Altmer", "Imperial", "Khajiit", "Nord", "Orc", "Redguard", "Bosmer"]
    specialization_list = ["Combat", "Magic", "Stealth"]
    favored_attributes_list = ["Strength", "Intelligence", "Willpower", "Agility", "Speed", "Endurance", "Personality", "Luck"]
    birthsign_list = ["The Apprentice", "The Atronach", "The Lady", "The Lord", "The Lover", "The Mage", "The Ritual", "The Serpent", "The Shadow", "The Steed", "The Thief", "The Tower", "The Warrior"]
    skills_list = ["Alchemy", "Alteration", "Armorer", "Athletics", "Axe", "Block", "Blunt Weapon", "Conjuration", "Destruction", "Enchant", "Hand-to-hand", "Heavy Armor", "Illusion", "Light Armor", "Long Blade", "Marksman", "Medium Armor", "Mercantile", "Mysticism", "Restoration", "Security", "Short Blade", "Sneak", "Spear", "Speechcraft", "Unarmored"]
    sex_list = ["Male", "Female"]

    keyed_args = {item.split('=')[0]: item.split('=')[1] for item in args[1:len(args)]}
    #could have parameters for all, but why generate a character when you know what you want?
    #stick to sex and race parameters
    if 'race' in keyed_args:
        if keyed_args['race'] in race_list:
            chosen_race = keyed_args['race']
        else:
            await message.channel.send(f"Cant recognize \'{keyed_args['race']}\'. Choosing race at random")
            chosen_race = random.choice(race_list)
    else:
        chosen_race = random.choice(race_list)
    
    if 'sex' in keyed_args:
        if keyed_args['sex'] in sex_list:
            chosen_sex = keyed_args['sex']
        else:
            await message.channel.send(f"Cant recognize \'{keyed_args['sex']}\'. Choosing sex at random")
            chosen_sex = random.choice(sex_list)
    else:
        chosen_sex = random.choice(sex_list)
    # Choose 1 specialization
    chosen_specialization = random.choice(specialization_list)
    
    # Choose 2 favored attributes (cannot choose the same twice)
    chosen_favored_attributes = random.sample(favored_attributes_list, 2)

    # Choose 5 major skills and 5 minor skills (no duplicates)
    chosen_skills = random.sample(skills_list, 10)
    chosen_major_skills = chosen_skills[:5]
    chosen_minor_skills = chosen_skills[5:]

    # Choose 1 birthsign
    chosen_birthsign = random.choice(birthsign_list)

    g = grammar.Grammar('grammar.gr')
    g.parseGrammar()
    chosen_name = 'none'
    if chosen_race == 'Dunmer':
        #sometimes take ashlander name
        if random.choice([True, False]):
            chosen_race = "Dunmer - Ashlander"
            chosen_name = g.generate_name(chosen_sex.lower(),'ashlander')
        else:
            chosen_name = g.generate_name(chosen_sex.lower(),chosen_race.lower())
    else:
        chosen_name = g.generate_name(chosen_sex.lower(),chosen_race.lower())
    

    out = "```\n"
    out = out + f"Name: {chosen_name}\n\n"
    out = out + f"Race: {chosen_race}\n\n"
    out = out + f"Sex: {chosen_sex}\n\n"
    out = out + f"Birthsign: {chosen_birthsign}\n\n"
    out = out + f"Specialization: {chosen_specialization}\n\n"
    out = out + f"Favored Attributes: {chosen_favored_attributes}\n\n"
    out = out + f"Major Skills: {chosen_major_skills}\n\n"
    out = out + f"Minor Skills: {chosen_minor_skills}"
    out = out + f"\n```"
    await message.channel.send(out)

async def command_commands(args, message, commandList):
    text = '```\n'
    for command in commandList:
        text = text + str(command)
        text = text + '\n'
    text = text + '```'
    await message.channel.send(text)

async def command_man(args, message, commandList):
    if len(args) == 1 or args[1] == 'man':
        await message.channel.send(
            "**$man Command**\n"
            "Usage: `$man <command>`\n"
            "Description: Provides detailed information about how to use a specified command.\n"
            "When `<command>` is specified, `$man` returns information such as the usage, description, "
            "parameters, and examples for the specified command.\n\n"
            "If `<command>` is `man`, this meta-command displays information about how to use the `$man` command itself.\n\n"
            "Example:\n"
            "```\n"
            "$man plot\n"
            "```\n"
            "This example would return detailed usage information about the `$plot` command, explaining how to use it, "
            "what parameters it accepts, and providing a sample command invocation."
        )
        return
     
    if args[1] == 'ping':
        await message.channel.send(
            "**$ping Command**\n"
            "Usage: `$ping`\n"
            "Description: Sends a simple message to test the responsiveness of the bot.\n"
            "Example:\n"
            "```\n"
            "$ping\n"
            "```\n"
            "The bot will respond with '**Pong!**' to indicate it is online and responsive."
        )
        return
    
    if args[1] == 'plot':
        await message.channel.send(
            "**$plot Command**\n"
            "Usage: `$plot [options]`\n"
            "Description: Plots a mathematical function based on specified parameters.\n"
            "Options:\n"
            "- `function=<function>`: Specifies the mathematical function to plot (e.g., `x**2`, `sin(x)`). default is `x`. DO NOT USE SPACES when defining a function\n"
            "- `from=<value>`: Specifies the starting value of the x-axis. Default is `-10`.\n"
            "- `to=<value>`: Specifies the ending value of the x-axis. Default is `10`.\n"
            "- `points=<integer>`: Specifies the number of points to calculate for the plot. Default is `100`.\n"
            "- `xTicks=<integer>`: Specifies the number of ticks on the x-axis. Defauilt is `auto`.\n"
            "- `yTicks=<integer>`: Specifies the number of ticks on the y-axis. Default is `auto`.\n"
            "- `grid=<true/false>`: Specifies whether to display a grid. Default is `false`.\n"
            "- `title=<string>`: Specifies graph title. Default is `Plot`.\n"
            "Example:\n"
            "```\n"
            "$plot function=sin(x) from=0 to=7 points=100 xTicks=10 yTicks=5 grid=true\n"
            "```\n"
            "This command will plot the sine function from 0 to 7, with a grid and specified ticks on the axes."
        )
        return

    if args[1] == 'commands':
        await message.channel.send(
            "**$commands Command**\n"
            "Usage: `$commands`\n"
            "Description: Lists available commands.\n"
            "Options: Takes no arguments.\n"
            "Example:\n"
            "```\n"
            "$commnads\n"
            "```\n"
            "This command will list all currently enabled commands."
        )
        return

    if args[1] == 'translate':
        await message.channel.send(
            "**$translate Command**\n"
            "Usage: `$translate from=<source_lang> to=<target_lang> text=\"<text to translate>\"`\n"
            "Description: Translates the specified text from the source language to the target language.\n"
            "Options:\n"
            "- `from=<source_lang>`: Specifies the ISO 639-1 code of the source language.\n"
            "- `to=<target_lang>`: Specifies the ISO 639-1 code of the target language.\n"
            "- `text=\"<text to translate>\"`: The text to be translated. Ensure the text is enclosed in double quotes.\n"
            "Examples:\n"
            "```\n"
            "$translate from=en to=es text=\"Hello, how are you?\"\n"
            "```\n"
            "The first example translates 'Hello, how are you?' from English to Spanish. The second example lists all supported languages."
        )
        return

    if args[1] == 'sort':
        await message.channel.send(
            "**$sort Command**\n"
            "Usage: `$sort data=<list> mode=<mode>`\n"
            "Description: Sorts a list of elements in ascending or descending order.\n"
            "Options:\n"
            "- `data=<list>`: A comma-separated list of elements to be sorted.\n"
            "- `mode=<mode>`: Specifies the sorting mode; 'up' for ascending (default) or 'down' for descending.\n"
            "Example:\n"
            "```\n"
            "$sort data=5,2,9,1 mode=up\n"
            "```\n"
            "This command sorts the numbers [5, 2, 9, 1] in ascending order."
        )
        return

    if args[1] == 'roll':
        await message.channel.send(
            "**$roll Command**\n"
            "Usage: `$roll [sides=<number>] [count=<number>]`\n"
            "Description: Rolls a specified number of dice with a specified number of sides and returns the results.\n"
            "Options:\n"
            "- `sides=<number>`: Specifies the number of sides on each die. Default is `6`.\n"
            "- `count=<number>`: Specifies the number of dice to roll. Default is `1`.\n"
            "Example:\n"
            "```\n"
            "$roll sides=20 count=3\n"
            "```\n"
            "This command will roll three 20-sided dice and return the results."
        )
        return

    if args[1] == 'morrowgen':
        await message.channel.send(
            "**$morrowgen Command**\n"
            "Usage: `$morrowgen [options]`\n"
            "Description: Generates a random character for the game Morrowind with various attributes and skills.\n"
            "Options:\n"
            "- `race=<race>`: Specifies the race of the character. If not specified, a random race is chosen.\n"
            "- `sex=<sex>`: Specifies the sex of the character ('Male' or 'Female'). If not specified, a random sex is chosen.\n"
            "Example:\n"
            "```\n"
            "$morrowgen race=Dunmer sex=Female\n"
            "```\n"
            "This command generates a random female Dunmer character with randomly selected attributes such as specialization, favored attributes, major skills, minor skills, and birthsign."
        )
        return
    await message.channel.send(f"I dont know what \"{args[1]}\" means.")
    return

# Command switcher
command_switch = {
    'ping': command_ping,
    'plot': command_plot,
    'translate': command_translate,
    'sort': command_sort,
    'roll': command_roll,
    'morrowgen': command_morrowgen,
    'commands': command_commands,
    'man': command_man,
}

async def execute(command, args, message, prefix, commandList):
    command_name = command[len(prefix):]
    if command_name in command_switch:
        await command_switch[command_name](args, message,commandList)
    else:
        await message.channel.send(f"I dont recognize \"{command}\" as a command.")
