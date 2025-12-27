import discord
from discord.ext import commands, tasks
import os
import random
import aiohttp
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)


class INI(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not webhookURL:
            pass
        else:
            webhook.send("initialise.py loaded")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        filepath = os.path.join("json","server", guild.id,".json")
        if not os.path.exits: 
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w')as f:
                
                with open("json/defaultServer.json", 'r')as r:
                    defaultData=json.load(r)
                data=defaultData["onServerJoin"]
                json.dump(data, f, indent=4)
    
    
    
        

async def setup(client):
    await client.add_cog(INI(client))

