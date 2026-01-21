import discord
from discord.ext import commands
import asyncio
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

class ToDoList(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not webhookURL:
            pass
        else:
            webhook.send("toDoList.py loaded")

    @commands.command(name="todo",help="Manage toDoList", aliases=["td","tdl","todolist"])
    async def toDo(self, ctx, action=None, *, task=None):
     try:
        embed=discord.Embed(title="To-Do List")
        embed.author.name=ctx.author.display_name
        embed.color=discord.Color.blue()
        try:
            embed.set_thumbnail(url=ctx.author.avatar.url)
        except:
            pass
        with open(f"json/server/{ctx.guild.id}.json/", "r") as f:
                serverFile=json.load(f)
        prefix=serverFile["prefix"][0]
        toDoList=serverFile.get("toDoList", [])
        try:
            toDoList=toDoList[f"{ctx.author.id}"]
        except KeyError:
            toDoList[f"{ctx.author.id}"]=[]
            toDoList=toDoList[f"{ctx.author.id}"]

        if action in ["add", "a"]:
            if task is None:
                await ctx.send("Please provide a task to add.")
                return
            toDoList.append([task, 0])
            embed.description=f'Task Added: {task}'
            with open(f"json/server/{ctx.guild.id}.json/", "w") as f:
                json.dump(serverFile, f, indent=4)

        elif action in ["done", "d"]:
            if task is None or not task.isdigit() or int(task) > len(toDoList):
                await ctx.send("Please provide a valid task number to mark as done.")
                return
            if toDoList[int(task)-1][1] == 1:
                toDoList[int(task)-1][1] = 0
                embed.description=f"{task} marked as undone."
            else:
                toDoList[int(task)-1][1] = 1
                embed.description=f"{task} marked as done."
            with open(f"json/server/{ctx.guild.id}.json/", "w") as f:
                json.dump(serverFile, f, indent=4)

        elif action in ["remove", "r"]:
            if task is None or not task.isdigit() or int(task) > len(toDoList):
                await ctx.send("Please provide a valid task number to remove.")
                return
            removed_task = toDoList.pop(int(task)-1)
            embed.description=f'Removed task: "{removed_task[0]}" from your to-do list.'
            with open(f"json/server/{ctx.guild.id}.json/", "w") as f:
                json.dump(serverFile, f, indent=4)
        elif action is None:
            pass
        else:
            await ctx.send("Use add, done or remove as the action!")
            await asyncio.sleep(1)
            
        if not toDoList:
            embed.description="Your to-do list is empty."
        else:
            i=1
            for x in toDoList:
                val=f"{x[0]} - {'✅' if x[1]==1 else '🟡'}"
                embed.add_field(name=f"{i}. ", value=val, inline=True)
                i += 1
        
        embed.set_footer(text=f"Use {prefix}todo add <task> to add a task, {prefix}todo done <task number> to mark as done, {prefix}todo remove <task number> to remove a task.")
        await ctx.send(embed=embed)
     except Exception as e:
         webhook.send(f"Error in toDoList.py: \n{e}")

async def setup(client):
    await client.add_cog(ToDoList(client))