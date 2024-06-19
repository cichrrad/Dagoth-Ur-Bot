
man_description =str(
    "**$ping Command**\n"
    "Usage: `$ping`\n"
    "Description: Sends a simple message to test the responsiveness of the bot.\n"
    "Example:\n"
    "```\n"
    "$ping\n"
    "```\n"
    "The bot will respond with '**Pong!**' to indicate it is online and responsive."
    )

async def run(message):
    await message.channel.send('**Pong!**')