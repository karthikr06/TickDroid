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

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not webhookURL:
            pass    
        else:
            webhook.send("ping.py loaded")

    
    @commands.command(
        name="ping",
        help="Checks the bot's latency", 
        aliases=['latency', 'lats'])
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000) # Latency in milliseconds
        await ctx.send(f"Pong! My latency is {latency}ms.")

    
    @commands.command(
        name="say",
        help="say stuff", 
        aliases=['s'])
    async def say(self, ctx, *, message):
        await ctx.send(f"{message}")

async def setup(client):
    await client.add_cog(Ping(client))

