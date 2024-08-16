import asyncio
import os

# Frames is a text file in the form [frame0 ascii art]\n#!\n[frame1 ascii art]\n#!\n[frame2 ascii art]...
# Does this suck ? Yes.
# Do I care ? No.

async def animate (message,frames,delta=200,loops=10):
    #parse frames
    frames = frames.split('\n#!\n')
    #send frame as a message, edit it and resend another after delta
    if len(frames) > 1:
        msg = await message.channel.send(".")
        for loop in range(0,loops):
            for frame in frames:
                #wait for 'delta' ms
                await asyncio.sleep(delta/1000)
                await msg.edit(content=f"```\n{frame}\n```")
    else:
        #not enough frames to do an animation
        await message.channel.send(f"```\n{frames[0]}\n```")
    return

