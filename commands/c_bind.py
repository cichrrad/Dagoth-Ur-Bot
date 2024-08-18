import py_stuff.send_wrapper as sw
import py_stuff.session_binding as sb
import os

man_description = str(
    "**$bind Command**\n"
    "Usage: `$bind [session type]`\n"
    "Description: Creates a session for multi-message/interactive commands. Allows each user to have 1 session per channel. Only registers authors messages in that channel.\n"
    "Valid session types are:\n"
    "```\n" + ', '.join(open('.session_names').read().splitlines()) + "```"
    "Example:\n"
    "```\n"
    "$bind shout\n"
    "```\n"
    "The bot will remove users messages and repeat them back in all-caps and bold."

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