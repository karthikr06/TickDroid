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
      try:
        with open(f"json/server/{str(ctx.guild.id)}.json", "r") as f:
            serverconfig=json.load(f)
        if serverconfig["features"]["ping"]==False:
            pass
        else:
            latency = round(self.client.latency * 1000) # Latency in milliseconds
            await ctx.send(f"Pong! My latency is {latency}ms.")
      except Exception as e:
            webhook.send(f"Error in ping command: \n```{e}```")

    
    #command #2
    @commands.command(
        name="say",
        help="say stuff", 
        aliases=['s'])
    async def say(self, ctx, *, message):
        await ctx.send(f"{message}")
        message.delete()

    #command #3
    @commands.command()
    async def addPrefix(self, ctx, *, new_prefix):
        guildID=ctx.guild.id
        with open(f"json/server/{guildID}.json", "r") as f:
            file=json.load(f)
        if ctx.author.id in file["admins"]:
            filepath = os.path.join("json","server",f"{str(guildID)}.json")

            #creating the file if it does not exist yet
            if not os.path.exists(filepath):
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w')as f:
                    with open("json/defaultServer.json", 'r')as r:
                        defaultData=json.load(r)
                    data=defaultData
                    json.dump(data, f, indent=4)
            
            #opening the file to find the prefixes
            with open(filepath, "r") as f:
                data=json.load(f)
            prefixes=data.get("prefix", [])
            if new_prefix in prefixes:
                await ctx.send(f"The prefix '{new_prefix}' is already in use.")
                return
            
            #adding the new prefix
            prefixes.append(new_prefix)
            data["prefix"]=prefixes
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send(f"Added new prefix: '{new_prefix}'")
        else:
            msg=await ctx.send("You do not have the permission to use this command.")
            await msg.delete(delay=5)

    #command #4
    @commands.command()
    async def removePrefix(self, ctx, prefix_to_remove):
        guildID=ctx.guild.id
        with open(f"json/server/{guildID}.json", "r") as f:
            file=json.load(f)
        if ctx.author.id in file["admins"]:
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
            if prefix_to_remove not in prefixes:
                await ctx.send(f"The prefix '{prefix_to_remove}' is not in use.")
                return
            if len(prefixes) == 1:
                await ctx.send("You cannot remove the last prefix")
            else:
                prefixes.remove(prefix_to_remove)
                data["prefix"]=prefixes
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                await ctx.send(f"Removed prefix: '{prefix_to_remove}'")
        else:
            msg=await ctx.send("You do not have the permission to use this command.")
            await msg.delete(delay=5)

    #command #5 
    @commands.command(aliases=['prefixes', 'listprefix'])
    async def listPrefixes(self, ctx):
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
        prefix_list = ', '.join(prefixes)
        await ctx.send(f"Current prefixes: {prefix_list}")
    

async def setup(client):
    await client.add_cog(commandClass(client))

