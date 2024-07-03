
async def wrapperSend(message, contents, mode='normal'):
    max_length = 1900
    parts = []

    # Split contents by the maximum length, attempting to end at a newline
    while len(contents) > max_length:
        split_at = max_length
        if '\n' in contents[:max_length]:
            split_at = contents.rfind('\n', 0, max_length) + 1
        parts.append(contents[:split_at])
        contents = contents[split_at:]

    parts.append(contents)  # Append the remainder of the contents
    total_parts = len(parts)
    
    for i, part in enumerate(parts, start=1):
        if mode == 'mono':
            part = f"```\n{part}\n```"
        if mode == 'ansi':
            part= f"```ansi\n{part}```"
        await message.channel.send(part)


async def wrapperSend_force_newline(message, contents, mode='normal'):
    max_length = 1900
    parts = []

    # Split contents by the maximum length, ensuring to end at a newline if possible
    while len(contents) > max_length:
        split_at = max_length
        newline_index = contents.rfind('\n', 0, max_length)
        if newline_index != -1:
            split_at = newline_index + 1
        parts.append(contents[:split_at])
        contents = contents[split_at:]

    parts.append(contents)  # Append the remainder of the contents
    total_parts = len(parts)
    
    for i, part in enumerate(parts, start=1):
        if mode == 'mono':
            part = f"```\n{part}\n```"
        if mode == 'ansi':
            part= f"```ansi\n{part}```"
        await message.channel.send(part)


async def wrapperSend_ansi(message, contents):
    max_length = 1900  # Adjusted for safe message size
    lines = contents.split('\n')
    current_message = "```ansi\n"

    for line in lines:
        # Check if adding the next line will exceed the max_length
        if len(current_message) + len(line) + len("\n```") > max_length:
            current_message += "```"  # Close the current message block
            await message.channel.send(current_message)
            current_message = "```ansi\n"  # Start a new message block
        
        current_message += line + "\n"

    current_message += "```"  # Close the last message block
    await message.channel.send(current_message)

