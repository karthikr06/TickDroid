import discord
from discord.ext import commands
import os
import asyncio
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if webhookURL:
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
        filepath = os.path.join("json","server", f"{str(guild.id)}.json")
        if not os.path.exists(filepath): 
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w')as f:
                with open("json/defaultServer.json", 'r')as r:
                    defaultData=json.load(r)
                json.dump(defaultData, f, indent=4)
    
    @commands.command(name="integrityCheck", help="Performs an integrity check on configuration files", aliases=['checkfiles'])
    async def integrityCheck(self, ctx):
     try:
      with open("json/botmods.json", "r") as f:
        config=json.load(f)
      if ctx.author.id in config["admin"]:
        created=0
        checked=0
        msg=await ctx.send("Performing Integrity check...")
        await asyncio.sleep(1)
        with open("json/control.json", 'r') as f:
            control=json.load(f)
        with open("json/defaultServer.json", 'r') as r:
            defaultData=json.load(r)
        
        #checking global control file
        for key in defaultData: #for all keys in defaultData
                    if key not in control:
                        control[key]=defaultData[key]
        for key in control: #for all keys in control
            if key not in defaultData:  
                del control[key]
        if control["prefix"]==[]:
            control["prefix"]=defaultData["prefix"]
        with open(f"json/control.json", 'w') as f:
            json.dump(control, f, indent=4)
        
        guildIDs=[guild.id for guild in self.client.guilds]
        for x in guildIDs:
            if os.path.exists(f"json/server/{str(x)}.json"):
                with open(f"json/server/{str(x)}.json", 'r') as f:
                    serverData=json.load(f)
                
                for key in defaultData: #for all keys in defaultData
                    if key not in serverData:
                        serverData[key]=defaultData[key]
                for key in serverData: #for all keys in serverData
                    if key not in defaultData:
                        del serverData[key]
                if serverData["prefix"]==[]:
                    serverData["prefix"]=defaultData["prefix"]
                    webhook.send(f"Reset empty prefix for server {x}")

                with open(f"json/server/{str(x)}.json", 'w') as f:
                    json.dump(serverData, f, indent=4)
                    checked+=1
                    
            else:
                filepath = os.path.join("json","server", f"{str(x)}.json")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w')as f:
                    with open("json/defaultServer.json", 'r')as r:
                        defaultData=json.load(r)
                    json.dump(defaultData, f, indent=4)
                    created+=1
        await msg.edit(content=f"Integrity check complete! Created {created} files, checked {checked} files.")
      else:
        webhook.send(f"User {ctx.author} ({ctx.author.id}) tried to use the integrity check command but was not authorised.")
     except Exception as e:
         webhook.send(f"Error occurred during Integrity check: \n{e}")


async def setup(client):
    await client.add_cog(INI(client))
