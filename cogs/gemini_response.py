import discord
from discord.ext import commands
from google import genai 
import json
from sarvamai import SarvamAI

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
        self.sarvam_client = SarvamAI(api_subscription_key=config.get("sarvam_api_key",""))

    async def get_gemini_response(self, prompt=None) -> str:
        if not prompt:
            prompt="Return a general greeting message."
        gemini_response_text=self.client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
        return gemini_response_text.text
    
    async def get_sarvam_response(self, prompt=None) -> str:
        if not prompt:
            prompt="Return a general greeting message."

        response = self.sarvam_client.chat.completions(
        messages=[{"role": "user", "content": f"{prompt}. Do not end the reply with a question."}],temperature=0.5, top_p=1, max_tokens=1000,)
        return response.choices[0].message.content


    #Fix this in next commit
    '''
    async def getAudioResponse(self, text=None) -> bytes:
        if True:
            device = 'auto'
            speed=1.0
            if not text:
                text="Hello, How are you doing today? Need any help from my end?"
            model=TTS(language="EN", device=device)
            speaker_ids=model.hps.data.spk2id
            output_path='en-br.wav'
            model.tts_to_file(text, speaker_ids['EN-BR'], output_path, speed=speed)
        else:
        
        
            if not text:
                text="Hello, How are you doing today? Need any help from my end?"
            audio_response=self.client.models.generate_content(model="gemini-3-flash-preview", contents=text, modalities=["text","audio"])
            return audio_response.audio.data
    '''
        
    

async def setup(client):
    await client.add_cog(GeminiCog(client))
