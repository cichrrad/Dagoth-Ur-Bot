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
    
    #read all possible session types from .session_names file
    with open('.session_names', 'r') as f:
        session_names = f.read().splitlines()
    
    if len(args) < 2:
        await sw.wrapperSend(message,"No session type provided. Valid session names are:\n```\n" + ', '.join(session_names)+'```')
        return
    _type = args[1].strip().lower()
    if _type not in session_names:
        await sw.wrapperSend(message,"Invalid session type provided. Valid session names are:\n```\n" + ', '.join(session_names)+'```')
        return
    await sw.wrapperSend(message,f"Starting **{_type}** session for **{message.author}**.")
    await sb.bind(message,_type)
    return