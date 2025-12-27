import discord
from discord.ext import commands
import os
from datetime import datetime
import requests
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix="t-")

if not webhookURL:
    pass
else:
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
    if not webhookURL:
        pass
    else:
        webhook.send("-------------")
        webhook.send(f"Logged in as {client.user}") 
    
    start_time = datetime.now()
    if not webhookURL:
        pass
    else:
        webhook.send(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}') 
            except Exception as e:
                if not webhookURL:
                    pass    
                else:
                    webhook.send(f"Failed to load cog {filename[:-3]}: {type(e).__name__}: {e}")
                    
    if not webhookURL:  
        pass    
    else:
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