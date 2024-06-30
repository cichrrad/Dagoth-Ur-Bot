import commands.send_wrapper as sw
import commands.option_parser as op

import discord

import io
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import numexpr as ne


man_description = str(
    "**$plot Command**\n"
    "Usage: `$plot [options] <(function)>`\n"
    "Description: `Plots a graph of a mathematical function.`\n"
    "Options:\n"
    "  -`start=<float>: set the start x coordinate. Default is -10.`\n"
    "  -`end=<float>: set the end x coordinate. Default is 10.`\n"
    "  -`points=<integer>: set the number of points to plot. Default is 100.`\n"
    "  -`xTicks=<integer>: set the number of ticks on the x axis. Default is auto.`\n"
    "  -`yTicks=<integer>: set the number of ticks on the y axis. Default is auto.`\n"
    "Example:\n"
    "```\n"
    "$plot start=0 end=5 points=100 xTicks=10 yTicks=5 (1-x**2)\n"
    "```\n"
)

options_table = [   [['start'], ['any_float'], ['-10']], 
                    [['end'], ['any_float'], ['10']], 
                    [['points'], ['any_int_positive'], ['100']], 
                    [['xTicks'], ['any_int_positive'], ['auto']], 
                    [['yTicks'], ['any_int_positive'], ['auto']]]

async def run(message):

    contents = message.content
    options = op.parse_command_options(contents, options_table)
    print(options)
    args = contents.split(' ',1)
    #if there is anything beside the command
    if len(args) > 1:
        #find beginning of list
        list_start = args[1].find('(')
        list_end = args[1].rfind(')')

        x = np.linspace(float(options['start']), float(options['end']), int(options['points']))
        
        expression = args[1][list_start+1:list_end]
        print (f"expression is {expression}")
        try:
            func = ne.evaluate(expression, local_dict={'x': x})
        except Exception as e:
            await message.channel.send(f"Failed to evaluate function '{expression}': {e}\n Make sure to surround function in parentheses")
            func = x
        
        plt.figure()
        plt.plot(x, func)
        if options['xTicks'] != 'auto':
            plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=options['xTicks']))
        if options['yTicks'] != 'auto':
            plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=options['xTicks']))
        plt.grid(True)

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)  # Rewind the buffer to the beginning so it can be read
        plt.close()  # Close the figure to free up memory
        await message.channel.send(file=discord.File(buf, 'plot.png'))
    else:
        await message.channel.send(man_description)