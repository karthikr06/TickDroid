import discord
from discord.ext import commands, tasks
import os
import json
import aiohttp

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

class General(commands.Cog):
        def __init__(self, client):
            self.client = client
            if not webhookURL:
                pass
            else:
                webhook.send("general.py loaded")
        
        @commands.Cog.listener()
        async def on_message(self, message):
            if message.author.bot:
                return

            if self.client.user.mentioned_in(message):
                content_after_mention = message.content.replace(f"<@{self.client.user.id}>", "").strip()

                #Is server existing in the database?
                guildID=message.guild.id
                filepath = os.path.join("json","server",f"{str(guildID)}.json")
                if not os.path.exists(filepath):
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'w')as f:
                        with open("json/defaultServer.json", 'r')as r:
                            defaultData=json.load(r)
                        data=defaultData
                        json.dump(data, f, indent=4)

                if not content_after_mention:
                    gemini_prompt = (
                        f"You are really helpful and kind Discord bot. Respond to a simple ping/mention with a concise, conversational greeting or acknowledgement that is helpful to them. Keep it to one or two sentences."
                    )
                else:
                    gemini_prompt = (
                        f"You are really helpful and kind Discord bot. The user said: '{content_after_mention}'. "
                        f"Provide a conversational, and helpful response (3-4 sentences) as if you are their friend."
                    )

                gemini_response_text = await self.client.get_cog('GeminiCog').get_gemini_response(gemini_prompt)

                embed = discord.Embed(
                    title=f"👋 Hello, {message.author.display_name}!",
                    description=f"{gemini_response_text}",
                    color=discord.Color.blue()
                )

                if message.author.avatar:
                    embed.set_thumbnail(url=message.author.avatar.url)

                bot_prefix = ""
                if isinstance(self.client.command_prefix, str):
                    bot_prefix = self.client.command_prefix
                elif isinstance(self.client.command_prefix, list) and self.client.command_prefix:
                    bot_prefix = self.client.command_prefix[0]
            
                embed.set_footer(text=f"My prefix is: {bot_prefix}")
                await message.reply(embed=embed)

        @commands.command()
        async def g(self,ctx,*, message=None):
                if not message:
                     message="Give me a personal greeting message"
                gemini_prompt=f"{message} Provide answer in 6-7 lines in a conversational and friendly style. Ignore line limit if you feel like it is not sufficient."
                gemini_response_text = await self.client.get_cog('GeminiCog').get_gemini_response(gemini_prompt)

                '''embed = discord.Embed(
                    title=f"{message}",
                    description=f"{gemini_response_text}",
                    color=discord.Color.blue()
                )

                if ctx.author.avatar:
                    embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text="Powered by Gemini 2.5 Flash")
                bot_prefix = ""
                if isinstance(self.client.command_prefix, str):
                    bot_prefix = self.client.command_prefix
                elif isinstance(self.client.command_prefix, list) and self.client.command_prefix:
                    bot_prefix = self.client.command_prefix[0]
            
                embed.set_footer(text=f"My prefix is: {bot_prefix}")
                #await ctx.reply(embed=embed)
                '''
                await ctx.reply(gemini_response_text)
        

async def setup(client):
    await client.add_cog(General(client))
