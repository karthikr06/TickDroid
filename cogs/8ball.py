import discord
from discord.ext import commands
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

class eightBall(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not webhookURL:
            pass
        else:
            webhook.send("8Ball.py loaded")

    @commands.command(
        name="eightball",
        help="Plays Magic 8-Ball",
        aliases=['8ball', '8b'])
    async def eightball(self, ctx,*, message: str):
        geminiPrompt=(f'''Give a reply for {message} as if you are a magic 8 ball that is optimistic and positive for positive things
                      and negative reply for negative things''')
        

        gemini_response_text = await self.client.get_cog('GeminiCog').get_gemini_response(geminiPrompt)

        embed = discord.Embed(
        title=f"{ctx.author.display_name}: {message}",
        description=f"{gemini_response_text}",
        color=discord.Color.blue() # You can choose any color you like
        )

        tip="✨Powered by Google Gemini"

        embed.set_footer(text=f"🎱Magic 8 Ball 🎱\n{tip}", )
        if ctx.author.avatar.url:
            embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(eightBall(client))

