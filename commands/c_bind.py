import py_stuff.send_wrapper as sw
import py_stuff.session_binding as sb
import os

man_description = str(
    "**$bind Command**\n"
    "Usage: `$bind`\n"
    "Description: Binds the current session to a user, channel, and guild. WIP, do not use, unless you know what you're doing\n"
)



async def run(message):
    #split message
    content = message.content
    args = content.split(' ', 1)
    # TODO - add error handling for no args
    _type = args[1]
    await sb.bind(message,_type)
    return