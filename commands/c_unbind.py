import py_stuff.send_wrapper as sw
import py_stuff.session_binding as sb
import os 

man_description = str(
    "**$unbind Command**\n"
    "Usage: `$unbind`\n"
    "Description: Unbinds the current session from a user, channel, and guild. WIP, do not use, unless you know what you're doing\n"
)

async def run(message):
    
    await sb.unbind(message)
    return