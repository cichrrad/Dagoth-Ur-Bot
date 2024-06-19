import wikipedia

import commands.send_wrapper as sw

# TODO handle branching to different wiki pages in case of ambiguity

man_description =str(
    "**$wiki Command**\n"
    "Usage: `$wiki <search term>`\n"
    "Description: Sends a summary of the search term's wiki page (given that it exists).\n"
    "Example:\n"
    "```\n"
    "$wiki The Elder Scrolls III: Morrowind\n"
    "```\n"
    "The bot will respond with the summary of the search term."
)

async def run(message):
    #anything after command is a search term
    contents = message.content
    args = contents.split(' ',1)
    default = 'The Elder Scrolls III: Morrowind'
    if len(args) >1:
        term = args[1].strip()
        print(f"searching for '{term}'")
    else:
        await message.channel.send("No search term provided.")
        term = default
    
    out = wikipedia.summary(term)
    await sw.wrapperSend(message,out,'mono')
    return