import discord
from discord.ext import commands
from google import genai 
import json

#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)


class GeminiCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("json/botmods.json", "r") as f:
            config=json.load(f)
        self.gemini_api_key=config.get("gemini_api_key","")
        if not self.gemini_api_key:
            print("Gemini API key not found in configuration.")
        
        if not webhookURL:
            pass
        else:
            webhook.send("gemini_response.py loaded")
        
        self.client=genai.Client(api_key=self.gemini_api_key)
    async def get_gemini_response(self, prompt=None) -> str:
        if not prompt:
            prompt="Return a general greeting message."
        gemini_response_text=self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return gemini_response_text.text

async def setup(client):
    await client.add_cog(GeminiCog(client))
