
# NOTE you need to create your own .todo file in the root directory of the bot (not in the commands folder)
# it is not included as the lists are stored in this folder in plain text (very secure) 

import commands.send_wrapper as sw
import os

man_description = str(
    "**$todo Command**\n"
    "Usage: `$todo <operation> <task>`\n"
    "Description: Adds / removes / lists tasks from the todo list.\n"
    "Operations:\n"
    "- `+ <task>`: Adds a task to the todo list.\n"
    "- `-[task endtry ID]`: Removes a task from the todo list.\n"
    "- `ls`: Lists all tasks in the todo list.\n"
    "- `wipe`: Removes all tasks from the todo list.\n"
)

async def run(message):
    author = message.author
    default_op = "ls"
    entry = -1
    contents = message.content
    args = contents.split(' ',1)
    if len(args) > 1:
        #parse message for operation
        params = (args[1].split(' ',1))
        op = (params[0]).strip()
        #check if there is an entry to add
        if len(params) > 1:
            task = (params[1]).strip()
            if op == "+" or op.lower() == "add":
                pass
            else:
                op = default_op
                await message.channel.send(f"Invalid input for 'operation': {op}. Using default = {default_op}")
        else:
            #no entry to add -> default to just listing
            if op[0] == "-" and op[1:].isdigit():
                entry = int(op[1:])
                pass
            elif op == "ls" or op.lower() == "list":
                #TODO
                pass
            elif op == "wipe" or op.lower() == "w":
                #TODO
                pass
            else:
                op = default_op  
    else:
        op = default_op

    todo_file = os.path.join('.todo', f'todo_{author}')
    if not os.path.exists(todo_file):
        await message.channel.send(f"**{author}**s list not found ==> created one")
        with open(todo_file, 'w') as f:
            pass
    if op == "+" or op.lower() == "add":
        with open(todo_file, 'a') as f:
                f.write(f"{task}\n")
                await sw.wrapperSend(message,f"**{author}** added \"{task}\" to his **TODO** list",'normal')
                return
    
    if op[0] == "-" and op[1:].isdigit():
        try:
            line = int(op[1:])
            with open(todo_file, 'r') as f:
                lines = f.readlines()
            with open(todo_file, 'w') as f:
                for i in range(len(lines)):
                    if i != line - 1:
                        f.write(lines[i])
                    elif i == line - 1:
                        text = lines[i]
                await message.channel.send(f"**{author}** removed \"{text}\" from his **TODO** list")
                return
        except (ValueError, IndexError):
            await message.channel.send(f"Invalid input for '-': {op}. Positive integers only in range of the list.")
        return

    if op == "ls" or op.lower() == "list":
        i = 1
        text = ''
        for line in open(todo_file, 'r'):
            text += f"{i}. {line}"
            i += 1
        await message.channel.send(f"```\n{text}\n```")
        return

    if op == "wipe" or op.lower() == "w":
        os.remove(todo_file)
        await message.channel.send(f"**{author}**s list wiped")
        return