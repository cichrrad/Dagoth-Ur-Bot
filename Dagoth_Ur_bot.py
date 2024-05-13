from email.message import Message
from multiprocessing.connection import Client
from site import ENABLE_USER_SITE
from tokenize import Double
from xml.etree.ElementTree import tostring


import discord
import Commands as commands
import configparser

intents = discord.Intents.default()
intents.message_content = True


# Load the configuration
config = configparser.ConfigParser()
config.read('.config')  # Make sure the filename matches your config file

# Retrieve values from the configuration file
command_prefix = config['DEFAULT']['key']  # Command prefix
bot_token = config['DEFAULT']['token']     # Bot token


bot_client = discord.Client(intents=intents)

@bot_client.event
async def on_ready():
    print(bot_client.user.name + " is online")

#message events
@bot_client.event
async def on_message(message):
    
    #always ingores itself
    if message.author == bot_client.user:
        return
    #if the message starts with '$' -> fetchCommand()
    if message.content.startswith(command_prefix):
        
        await commands.callCommand(message)
        

print(bot_token)
#LAST COMMAND - STARTS THE BOT
bot_client.run(str(bot_token))

