
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
            part= f"```ansi\n{part}\n```"
        await message.channel.send(part)
