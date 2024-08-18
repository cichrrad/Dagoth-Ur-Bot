import py_stuff.send_wrapper as sw
import py_stuff.session_binding as sb
import os 

man_description = str(
    "**$unbind Command**\n"
    "Usage: `$unbind`\n"
    "Description: Removes currently bound ongoing session (interactive/multi-message commands) for the user in this channel."    
)

async def run(message):
    
    await sb.unbind(message)
    return