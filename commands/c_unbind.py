import py_stuff.send_wrapper as sw
import os 

man_description = str(
    "**$unbind Command**\n"
    "Usage: `$unbind`\n"
    "Description: Unbinds the current session from a user, channel, and guild. WIP, do not use, unless you know what you're doing\n"
)

async def run(message):
    if f"{message.author},{message.channel},{message.guild}" not in open('.bound_sessions').read():
        await sw.wrapperSend(message,f"Session not bound for [{message.author}] in [{message.channel}] on [{message.guild}]")
        return
    await sw.wrapperSend(message,f"Session unbound for [{message.author}] in [{message.channel}] on [{message.guild}]")
    with open('.bound_sessions', 'r') as f:
        lines = f.readlines()
    with open('.bound_sessions', 'w') as f:
        for line in lines:
            if f"{message.author},{message.channel},{message.guild}" not in line:
                f.write(line)
    return