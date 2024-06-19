import importlib.util
import sys
import commands.send_wrapper as sw


man_description = str(
            "**$man Command**\n"
            "Usage: `$man <command>`\n"
            "Description: Provides detailed information about how to use a specified command.\n"
            "When `<command>` is specified, `$man` returns information such as the usage, description, "
            "parameters, and examples for the specified command.\n\n"
)

async def run(message):
    #anything after command is a search term
    contents = message.content
    args = contents.split(' ',1)
    default = 'man'
    #lookup the command .py file
    if len(args) > 1:
        # check if the command is present in a file ".command_names"
        try:
            with open('.command_names', 'r') as f:
                command_names = f.read().splitlines()
        except FileNotFoundError:
            command_names = []

        if (args[1].lower()).strip() in command_names:
            man = (args[1].lower()).strip()
        else:
            man = default
            await message.channel.send(f"Invalid input. Using default = {default}.")
    else:
        man = default
    
    spec = importlib.util.spec_from_file_location(  
        "commands.c_" + man,
        f"commands/c_{man}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["commands.c_" + man] = module
    spec.loader.exec_module(module)
    
    out = getattr(module, 'man_description', "man description for \'"+str(man)+"\' not found")
    await message.channel.send(out)
    