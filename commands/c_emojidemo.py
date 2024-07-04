import commands.send_wrapper as sw

async def run(message):
    emoji_pallete = str("🟥🟧🟨🟩🟦🟪🟫⬛⬜")
    await sw.wrapperSend(message, emoji_pallete, 'normal')
    await sw.wrapperSend(message, emoji_pallete, 'mono')

