import commands.send_wrapper as sw

man_description=str(
    "**$sort Command**\n"
    "Usage: `$sort <list>`\n"
    "Description: `sorts a list of numbers separated by commas. use '.' for decimal points.`\n"
)

async def run(message):
    contents = message.content
    #get arguments
    args = contents.split(' ',1)

    #if there is anything beside the command
    if len(args) > 1:
        #get the list
        l = (args[1].split(','))
        #sort the list
        l = list(map(float, l))
        l.sort()
        #send the list
        await sw.wrapperSend(message, l, 'mono')
    else:
        await message.channel.send(man_description)
