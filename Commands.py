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
import numpy as np

#VARIABLES========================================================================
commandList = ['$ping','$plot']
#,'$commands','$cpp','$java','$ascii','$ascii_fonts','$sort']
ascii_art_fonts = pyfiglet.FigletFont.getFonts()
defualt_font = "univers"
#VARIABLES========================================================================



#core func
async def callCommand(message):
    
    #just to be sure
    message_raw = (message.content).strip()
    args = message_raw.split()
    print(args)

    #identify the command
    if args[0] in commandList:
        await execute(args[0],args,message);
        return
    await message.channel.send(f'I dont recognize \"' + str(args[0]) +'\" as a command.')
    return

async def execute(command,args,message):
    #execute the command
    if command == '$ping':
        await message.channel.send('**Pong!**')
        return
    
    if command == '$plot':
        #defaults
        x_start = 0
        x_end = 10
        points = 100
        x_label = 'x'
        y_label = 'f(x)'
        title = 'Plot'
        
        #parsing user args
        keyed_args = {item.split('=')[0]: item.split('=')[1] for item in args[1:len(args)]}
        print(f"Parsed arguments are: {keyed_args}")
        if len(keyed_args) > 0:
            if 'from' in keyed_args:
                if keyed_args['from'].isnumeric():
                    x_start = keyed_args['from']
            if 'to' in keyed_args:
                if keyed_args['to'].isnumeric():
                    x_end = keyed_args['to']
            if 'points' in keyed_args:
                if keyed_args['points'].isnumeric():
                    points = keyed_args['points']
                    
                

        #plot
        x = np.linspace(int(x_start), int(x_end), int(points)) 
        func = x*x
        plt.figure()
        plt.plot(x, func)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)  # Rewind the buffer to the beginning so it can be read
        plt.close()  # Close the figure to free up memory
        await message.channel.send(file=discord.File(buf, 'plot.png'))

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
