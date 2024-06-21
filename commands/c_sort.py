import commands.send_wrapper as sw
import commands.option_parser as op

man_description=str(
    "**$sort Command**\n"
    "Usage: `$sort [options] (<list>)`\n"
    "Description: `sorts a list of elements within brackets.`\n"
    "Options:\n"
    "  -`mode=<up/down>: set sorting direction`\n"
    "  -`separator=<separator>: set the separator between elements. Default is ','.`\n"
    "Example:\n"
    "```\n"
    "$sort mode=up separator=, (1,2,3,4,5)\n"
    "```\n"
)


options_table = [[['mode'], ['up', 'down'], ['up']], [['separator'], [42], [',']]]


async def run(message):
    contents = message.content
    #parse options
    options = op.parse_command_options(contents, options_table)

    args = contents.split(' ',1)
    #if there is anything beside the command
    if len(args) > 1:
        #find beginning of list
        list_start = args[1].find('(')
        list_end = args[1].find(')')
        #if there is a list
        if list_start != -1 and list_end != -1:
            #get list
            l = args[1][list_start+1:list_end]
            #parse list
            l = l.split(options['separator'])
            #sort list
            if options['mode'] == 'up':
                l.sort()
            else:
                l.sort(reverse=True)
            #send list
            await sw.wrapperSend(message, ' , '.join(l), 'mono')
        else:
            await message.channel.send("No list found.")
    else:
        await message.channel.send(man_description)
