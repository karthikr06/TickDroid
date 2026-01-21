import discord
from discord.ext import commands
import os
from datetime import datetime
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

# Function to get server-specific prefix
def get_prefix(bot, message):
    # If in DM, use default prefix
    if not message.guild:
        with open("json/defaultServer.json", "r") as f:
            file = json.load(f)
        prefix = file.get("prefix")
        return prefix #default prefix for DMs.
                      #DM commands and messages are a WIP and may not work properly
    
    # Try to load server specific prefix
    filepath = f"json/server/{message.guild.id}.json"
    try:
        with open(filepath, "r") as f:
            file = json.load(f)
        prefix = file.get("prefix")

    except FileNotFoundError:
        #creating the file if not found and setting it to default data
        print(f"Created {filepath} since it was not found.")
        filepath = os.path.join("json","server",f"{str(message.guild.id)}.json")
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w')as f:
                with open("json/defaultServer.json", 'r')as r:
                    defaultData=json.load(r)
                data=defaultData
                json.dump(data, f, indent=4)
        prefix = data.get("prefix")
        #Note: Add self mention also here. will be useful.
        #Currently, a simple ping is given in general.py where it responds easily
    return prefix


#Discord intents here. message_content is needed for the bot to work with messages
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix=get_prefix, case_insensitive=True)

if webhookURL:
    webhook.send("Bot is starting...")

def checkMod(user, type="admin"): #checking if user is a bot mod
 try:
    with open('json/botmods.json', 'r')as f:
        f=json.load(f)
    if user in f[type]:
        return True
    else:
        return False
 except FileNotFoundError:
     print("Error occurred. Run setup again to fix the issue.")
    
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    if webhookURL:
        webhook.send("-------------")
        webhook.send(f"Logged in as {client.user}") 
    
    start_time = datetime.now()
    if webhookURL:
        webhook.send(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}') 
            except Exception as e:
                if webhookURL:
                    webhook.send(f"Failed to load cog {filename[:-3]}: {type(e).__name__}: {e}")
                    
    if webhookURL:
        webhook.send("-------------")



@client.command()
async def load(ctx, extension: str):
  if checkMod(ctx.author.id, 'admin'):
    # Check if the file exists
    filepath = f'cogs/{extension}.py'
    if not os.path.exists(filepath):
        await ctx.send("Check file name and try again")
        return
    
    try:
        await client.load_extension(f'cogs.{extension}')
        if webhookURL:
            webhook.send(f'Cog {extension} loaded successfully')
    except commands.ExtensionNotFound:
        await ctx.send("Check file name and try again")
        if webhookURL:
            webhook.send(f'Error: Cog `{extension}` not found.')
    except commands.ExtensionAlreadyLoaded:
        if webhookURL:
            webhook.send(f'Error: Cog `{extension}` is already loaded.')
    except Exception as e:
        if webhookURL:
            webhook.send(f'An error occurred while loading `{extension}`: ```{e}```')

@client.command()
async def unload(ctx, extension: str):
  if checkMod(ctx.author.id, 'admin'):
    try:
        await client.unload_extension(f'cogs.{extension}')
        
        if webhookURL:
            webhook.send(f'Cog `{extension}` unloaded successfully.')
    except commands.ExtensionNotLoaded:
        if webhookURL:
            webhook.send(f'Error: Cog `{extension}` is not loaded.')
    except Exception as e:
        if webhookURL:
            webhook.send(f'An error occurred while unloading `{extension}`: ```{e}```')

@client.command()
async def reload(ctx, extension: str):
  if checkMod(ctx.author.id, 'admin'):
    # Check if the file exists
    filepath = f'cogs/{extension}.py'
    if not os.path.exists(filepath):
        await ctx.send("Check file name and try again")
        return
    
    try:
        await client.reload_extension(f'cogs.{extension}')
        if webhookURL:
            webhook.send(f'Cog `{extension}` reloaded successfully.')
    except commands.ExtensionNotLoaded:
        if webhookURL:
            webhook.send(f'Error: Cog `{extension}` not loaded.')
    except Exception as e:
        if webhookURL:
            webhook.send(f'An error occurred while reloading `{extension}`: ```{e}```')

client.run(config.get("bot_token",""))