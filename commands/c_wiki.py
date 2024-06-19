import wikipedia
async def run(message):
    #anything after command is a search term
    contents = message.content
    term = (contents.split(' ',1))[1]
    print(f"searching for '{term}'")
    if term == []:
        term = 'The elder scrolls III: Morrowind'
        await message.channel.send("No search term provided.")
        out = wikipedia.summary(term)
        await message.channel.send(out)
    else:
        out = wikipedia.summary(term)
        await message.channel.send(out)
    
    return