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


#VARIABLES========================================================================
ascii_art_fonts = pyfiglet.FigletFont.getFonts()
defualt_font = "univers"
#VARIABLES========================================================================



#core func
async def callCommand(message,prefix):
    
    #just to be sure
    commandList = [f"{prefix}ping",f"{prefix}plot",f"{prefix}man",f"{prefix}commands",f"{prefix}translate"]
    message_raw = (message.content).strip()
    args = shlex.split(message_raw)
    print(args)

    #identify the command
    if args[0] in commandList:
        await execute(args[0],args,message,prefix,commandList);
        return
    await message.channel.send(f'I dont recognize \"' + str(args[0]) +'\" as a command.')
    return

async def execute(command,args,message,prefix,commandList):
    #execute the command
    if command == f"{prefix}ping":
        await message.channel.send('**Pong!**')
        return
    
    if command == f"{prefix}plot":
        #defaults
        x_start = -10
        x_end = 10
        points = 100
        x_label = 'x'
        y_label = 'f(x)'
        x_ticks = 'auto'  # Default number of ticks on the x-axis
        y_ticks = 'auto'  # Default number of ticks on the y-axis
        title = 'Plot'
        x = np.linspace(int(x_start), int(x_end), int(points))
        func = x
        show_grid = True
        
        
        #parsing user args
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

        #plot
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

    if command == f"{prefix}man":
        
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


        await message.channel.send(f"I dont know what \"{args[1]}\" means.")
        return

    if command == f"{prefix}commands":
        text = '```\n'
        for command in commandList:
            text = text + str(command)
            text = text + '\n'
        text = text + '```'
        await message.channel.send(text)

    if command == f"{prefix}translate":

        if len(args) >= 4: 
            from_lang = args[1].split('=')[1]
            to_lang = args[2].split('=')[1]
            text = args[3].split('=')[1]

            translator = Translator(from_lang=from_lang, to_lang=to_lang)
            translation = translator.translate(text)
            if 'INVALID SOURCE LANGUAGE' in translation:
                translation = f"Bad language code. See ```https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes```";
                await message.channel.send(f'{translation} (set 1) column.')
                return
            await message.channel.send(f'Translated Text: {translation}')
            return
        else:
            await message.channel.send("Usage: `$translate from=<language> to=<language> text=\"<text to translate>\"`")
            return
        

#    if cID == 1:
#        
#        comL ="```\n"
#        for i in commandList:
#            comL = comL + str(i) +"\n"  
#        comL = comL + "\n```"
#       
#        await message.channel.send(comL)
#        return
#
#    if cID == 2:
#        
#        code ="```cpp\n" + str(message.content).replace(str(commandList[2]),'') + "\n```"
#        code = code.strip()
#        await message.delete()
#        await message.channel.send(code)
#        return
#
#    if cID == 3:
#        
#        code ="```java\n" +str(message.content).replace(str(commandList[3]),'') +"\n```"
#        code = code.strip()
#        await message.delete()
#        await message.channel.send(code)
#        return
#
#    if cID == 4:
#
#        input_text = (message.content).replace(str(commandList[4]),'')
#        selected_font = defualt_font
#
#        for FOND in ascii_art_fonts:
#            if ('$'+str(FOND)) in input_text:
#                input_text = input_text.replace(('$'+str(FOND)),'')
#                selected_font = str(FOND)
#                break
#        
#        input_text = input_text.strip()
#        ascii_text = pyfiglet.figlet_format(input_text,font=selected_font)
#        await message.delete()
#        await message.channel.send("```"+ascii_text+"```")
#        return
#
#    if cID == 5:
#        
#        fontL ="```\n"
#        for FOND in ascii_art_fonts:
#            if(len(fontL) >= 1980):
#                await message.channel.send(fontL+"\n```")
#                fontL = "```\n"
#            fontL = fontL + str(FOND) + "\n"
#        fontL = fontL + "\n```"
#        await message.channel.send(fontL)
#    if cID == 6:
#        
#        input_text = message.content.replace(str(commandList[6]),'').strip()
#        
#        if ('$d') in input_text:
#            input_text = input_text.replace('$d','')
#            elements = input_text.split(',')
#            elements = [int(element) for element in elements]
#            elements.sort(reverse=True);
#            await message.delete()
#            await message.channel.send("```\n"+str(elements)+"\n```")
#            return
#        if ('$a') in input_text:
#            input_text = input_text.replace('$a','')
#            elements = input_text.split(',')
#            elements = [int(element) for element in elements]
#            elements.sort();
#            await message.delete()
#            await message.channel.send("```\n"+str(elements)+"\n```")
#            return
#        elements = input_text.split(',')
#        elements = [int(element) for element in elements]
#        elements.sort();
#        await message.delete()
#        await message.channel.send("```\n"+str(elements)+"\n```")
#        return
