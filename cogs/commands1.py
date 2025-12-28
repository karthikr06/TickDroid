import os
import json
import discord
from discord.ext import commands

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

class commandClass(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not webhookURL:
            pass    
        else:
            webhook.send("Commands #1 loaded")

    
    #command #1
    @commands.command(
        name="ping",
        help="Checks the bot's latency", 
        aliases=['latency', 'lats'])
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000) # Latency in milliseconds
        await ctx.send(f"Pong! My latency is {latency}ms.")

    
    #command #2
    @commands.command(
        name="say",
        help="say stuff", 
        aliases=['s'])
    async def say(self, ctx, *, message):
        await ctx.send(f"{message}")

    #command #3
    @commands.command()
    async def addPrefix(self, ctx, new_prefix):
        """Adds a new prefix for the server."""
        guildID=ctx.guild.id
        filepath = os.path.join("json","server",f"{str(guildID)}.json")
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w')as f:
                with open("json/defaultServer.json", 'r')as r:
                    defaultData=json.load(r)
                data=defaultData
                json.dump(data, f, indent=4)
        with open(filepath, "r") as f:
            data=json.load(f)
        prefixes=data.get("prefix", [])
        if new_prefix in prefixes:
            await ctx.send(f"The prefix '{new_prefix}' is already in use.")
            return
        prefixes.append(new_prefix)
        data["prefix"]=prefixes
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"Added new prefix: '{new_prefix}'")

async def setup(client):
    await client.add_cog(commandClass(client))

