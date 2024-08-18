from email.message import Message
from multiprocessing.connection import Client
from site import ENABLE_USER_SITE
from tokenize import Double
from xml.etree.ElementTree import tostring
import importlib.util
import sys
from types import ModuleType
from typing import Any
import asyncio
import os

import py_stuff.send_wrapper as sw
import py_stuff.session_binding as sb
import discord
#import Commands_core as commands
import configparser

intents = discord.Intents.default()
intents.message_content = True

# Load the configuration
config = configparser.ConfigParser()
config.read('.config')  # Make sure the filename matches your config file

# Retrieve values from the configuration file
command_prefix = config['DEFAULT']['key']  # Command prefix
bot_token = config['DEFAULT']['token']     # Bot token

command_names = []
for file in os.listdir('./commands/'):
    if file.endswith('.py') and file.startswith('c_'):
        command_names.append(file[2:-3])
print(f"Commands found: {command_names}")

session_names = []
for file in os.listdir('./sessions/'):
    if file.endswith('.py') and file.startswith('s_'):
        session_names.append(file[2:-3])
print(f"Session commands (interactive/multi message commands) found: {session_names}")

# Save command_names to .command_names file
with open('.command_names', 'w') as f:
    f.write('\n'.join(command_names))

# Save session_names to .session_names file
with open('.session_names', 'w') as f:
    f.write('\n'.join(session_names))


bot_client = discord.Client(intents=intents)

async def run_function_from_file(file_path: str, *args: Any) -> Any:
    """
    Imports a Python file, finds the 'run' function, and executes it with the provided arguments.
    
    :param file_path: Path to the Python file
    :param args: Arguments to pass to the 'run' function
    :return: The return value from the 'run' function, if any
    """
    # Load the module
    module_name = file_path.replace('.py', '').replace('/', '.').replace('\\', '.')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load module from {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ImportError(f"Could not import module from {file_path}: {e}")
    
    # man = getattr(module, 'man_description', None)
    # print(man)
    
    # Get the 'run' function
    run_function = getattr(module, 'run', None)
    if run_function is None:
        raise AttributeError(f"No 'run' function found in {file_path}")
    
    # Call the 'run' function with the provided arguments
    return await run_function(*args)

@bot_client.event
async def on_ready():
    print(f'{bot_client.user.name} is online')

@bot_client.event
async def on_message(message):
    # Always ignore itself
    if message.author == bot_client.user:
        return
    print(f"getting message from [{message.author}] in channel [{message.channel}] in discord server [{message.guild}]")
    print(f"message content: {message.content}")

    # If the message starts with the command prefix, fetch and run the command
    if message.content.startswith(command_prefix):
        command = message.content.split(' ')[0][len(command_prefix):].lower()
        print(f"Looking up '{command}' in known commands...")
        if command in command_names:
            print(f"Found '{command}' in known commands...")
            try:
                #each message command spawns a new task -> bot should be able to handle multiple commands at once
                await asyncio.create_task(run_function_from_file(f'./commands/c_{command}.py', message))
                print(f"Finished running '{command}'")
            except Exception as e:
                print(f"Error running '{command}': {e}")
                await message.channel.send(f"An error occurred while executing the command '{command}'.")
        else:
            print(f"Did not find '{command}' in known commands...")
            await message.channel.send(f"I don't recognize \"{command}\" as a command.")
    
    #process sessions, if the author has one ongoing in this channel
    if f"{message.author}:{message.channel}:{message.guild}" in open('.bound_sessions').read():
        #identify session type
        for line in open('.bound_sessions').readlines():
            if f"{message.author}:{message.channel}:{message.guild}" in line:
                session_type = line.split(':')[3].replace('\n','')
        print(f"Found ongoing session of type {session_type} for {message.author} in {message.channel} on {message.guild}")
        try:
            await asyncio.create_task(run_function_from_file(f'./sessions/s_{session_type}.py', message))
            print(f"Finished running session of type {session_type}")
        except Exception as e:
            print(f"Error running session of type {session_type}: {e}")

# Start the bot
bot_client.run(bot_token)
