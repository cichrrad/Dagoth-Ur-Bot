import py_stuff.send_wrapper as sw
import os
#handles session binding - creates sessions for multi-message/interactive commands
#identifies sessions by author, channel, and guild 
# --> each user can have one ongoing session in any given channel

#each session information is stored in a line in .bound_sessions
#format: "{message.author}:{message.channel}:{message.guild}:{session command}:{session command details}\n"

async def bind(message,_type):
    #note - .bound_sessions is in the root dir -> ../ from here
    if f"{message.author}:{message.channel}:{message.guild}" in open('.bound_sessions').read():
        currType = open('.bound_sessions').readlines()[0].split(':')[3].replace('\n','')
        await sw.wrapperSend(message,f"Session of type **{currType}** already bound for **{message.author}** in **{message.channel}** on **{message.guild}**.\nOnly one session per user in a given channel is allowed.")
        for line in open('.bound_sessions').readlines():
            if f"{message.author}:{message.channel}:{message.guild}" in line:
                print (line)
        return
    # await sw.wrapperSend(message,f"Session bound for [{message.author}] in [{message.channel}] on [{message.guild}]")
    with open('.bound_sessions', 'a') as f:
        f.write(f"{message.author}:{message.channel}:{message.guild}:{_type}\n")
    return

async def unbind(message):
    
    if f"{message.author}:{message.channel}:{message.guild}" not in open('.bound_sessions').read():
        await sw.wrapperSend(message,f"Nothing to unbind.")
        return
    await sw.wrapperSend(message,f"Session unbound for **{message.author}** in **{message.channel}** on **{message.guild}**")
    with open('.bound_sessions', 'r') as f:
        lines = f.readlines()
    with open('.bound_sessions', 'w') as f:
        for line in lines:
            if f"{message.author}:{message.channel}:{message.guild}" not in line:
                f.write(line)
    return