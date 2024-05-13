from email.message import Message
from multiprocessing.connection import Client
from site import ENABLE_USER_SITE
from tokenize import Double
from xml.etree.ElementTree import tostring
import discord
import requests
import pyfiglet

#VARIABLES========================================================================
commandList = ['$ping','$commands','$cpp','$java','$ascii','$ascii_fonts','$sort']
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
