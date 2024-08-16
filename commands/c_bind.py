import py_stuff.send_wrapper as sw
import os

man_description = str(
    "**$bind Command**\n"
    "Usage: `$bind`\n"
    "Description: Binds the current session to a user, channel, and guild. WIP, do not use, unless you know what you're doing\n"
)



async def run(message):
    
    #add "{message.author},{message.channel},{message.guild}" to .bound_sessions

    if f"{message.author},{message.channel},{message.guild}" in open('.bound_sessions').read():
        await sw.wrapperSend(message,f"Session already bound for [{message.author}] in [{message.channel}] on [{message.guild}]")
        return
    await sw.wrapperSend(message,f"Session bound for [{message.author}] in [{message.channel}] on [{message.guild}]")
    with open('.bound_sessions', 'a') as f:
        f.write(f"{message.author},{message.channel},{message.guild}\n")