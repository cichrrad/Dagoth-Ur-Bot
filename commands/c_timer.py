import commands.send_wrapper as sw
import asyncio

man_description = str(
    "**$timer Command**\n"
    "Usage: `$timer <value><unit> ...`\n"
    "Description: Starts a timer for the specified amount of time. \n"
    "Example:\n"
    "```\n"
    "$timer 1h(/hr/hours) 10m(/min/minutes) 20s(/sec/seconds) \n"
    "```\n"
    "The bot will respond with 'Timer started!' and 'Timer over', once the timer is over.\n"
)


async def run(message):

    contents = message.content
    def_hours = 0
    def_minutes = 0
    def_seconds = 0
    #split off the command
    args = contents.split(' ',1)


    #split the rest to look for data
    if len(args) > 1:
        time_data = args[1].split(' ')
        for time in time_data:
            time = time.lower()
            if time.endswith('h') or time.endswith('hr') or time.endswith('hours'):
                if time.endswith('h'):
                    def_hours = int(time[:-1])
                elif time.endswith('hr'):
                    def_hours = int(time[:-2])
                else:
                    def_hours = int(time[:-5]) 
                
                if def_hours < 0:
                    def_hours = -1*def_hours
            elif time.endswith('m') or time.endswith('min') or time.endswith('minutes'):
                if time.endswith('m'):
                    def_minutes = int(time[:-1])
                elif time.endswith('min'):
                    def_minutes = int(time[:-3])
                else:
                    def_minutes = int(time[:-7])
                
                if def_minutes < 0:
                    def_minutes = -1*def_minutes
            elif time.endswith('s') or time.endswith('sec') or time.endswith('seconds'):
                if time.endswith('s'):
                    def_seconds = int(time[:-1])
                elif time.endswith('sec'):
                    def_seconds = int(time[:-3])
                else:
                    def_seconds = int(time[:-7])
                
                if def_seconds < 0:
                    def_seconds = -1*def_seconds
            else:
                await message.channel.send("Invalid time unit. Try again.")
                return
        print(f"{def_hours}\n{def_minutes}\n{def_seconds}")

        msg = await message.channel.send(f"Timer started. Duration is {def_hours}h {def_minutes}m {def_seconds}s.")
        asyncio.create_task(timer_task(def_hours*60*60+def_minutes*60+def_seconds,msg))
    else:
        await message.channel.send(man_description)
        return



async def timer_task(countdown,msg):
    while countdown > 0:
        countdown -= 1
        await asyncio.sleep(1)
        
    await msg.reply("Done!") 