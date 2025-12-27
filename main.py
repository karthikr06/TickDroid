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

# Function to get server-specific prefix
def get_prefix(bot, message):
    # If in DM, use default prefix
    if not message.guild:
        with open("json/defaultServer.json", "r") as f:
            default_config = json.load(f)
        prefix = default_config.get("prefix")
        return prefix
    
    # Try to load server-specific prefix
    filepath = f"json/server/{message.guild.id}.json"
    try:
        with open(filepath, "r") as f:
            server_config = json.load(f)
        prefix = server_config.get("prefix")

    except FileNotFoundError:
        #creating the file if not found
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
    return prefix

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix=get_prefix)

if webhookURL:
    webhook.send("Bot is starting...")

def checkMod(user, type):
    with open('json/botmods.json', 'r')as f:
        f=json.load(f)
    if user in f[type]:
        return True
    else:
        return False
    
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
    try:
        await client.load_extension(f'cogs.{extension}')
        if webhookURL:
            webhook.send(f'Cog {extension} loaded successfully')
    except commands.ExtensionNotFound:
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