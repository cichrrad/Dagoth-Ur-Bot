import commands.send_wrapper as sw

man_description = str(
    "**$list Command**\n"
    "Usage: `$list`\n"
    "Description: Lists all known commands.\n"
)

async def run(message):
    try:
        with open('.command_names', 'r') as f:
            command_names = f.read().splitlines()
    except FileNotFoundError:
        await message.channel.send("No commands found")
        return

    await sw.wrapperSend(message, "\n".join(command_names), 'mono')