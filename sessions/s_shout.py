import py_stuff.send_wrapper as sw



async def run(message):
    #delete user message and repeat it in all caps and bold
    temp = message
    await message.delete()
    await sw.wrapperSend(temp,f"**{temp.content.upper()}**")
    return