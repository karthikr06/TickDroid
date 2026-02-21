import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from google import genai
from google.genai import types
import json
import io
import os
import azure.cognitiveservices.speech as speechsdk



#getting the configuration file
with open("json/botmods.json", "r") as f:
    config=json.load(f)
webhookURL=config.get("webookURL","")
if not webhookURL:
    pass
else:
    webhook=discord.SyncWebhook.from_url(webhookURL)

genAI_client=genai.Client(api_key=config.get("gemini_api_key",""))


class pdfButtons(discord.ui.View):
    def __init__(self, attachment:discord.Attachment, bot_message:discord.Message=None, msgID:int=None):
        super().__init__(timeout=120)
        self.attachment = attachment
        self.bot_message = bot_message
        self.msgID = msgID

    def set_bot_message(self, bot_message:discord.Message):
        self.bot_message = bot_message

    @discord.ui.button(label="Summarise", style=discord.ButtonStyle.blurple,emoji="📄")
    async def summarise(self, interaction:discord.Interaction, button:discord.ui.Button):
        #acknowledging the interaction, but defer the response 
        #if this code does not exist, then interaction failed error might occur
        await interaction.response.defer()
        if self.bot_message:
            try:
                await self.bot_message.edit(content=f"Processing {self.attachment.filename}...", view=None)
            except Exception:
                pass
    
        try:
            file_data=await self.attachment.read()
            iofile=io.BytesIO(file_data)
            upload=genAI_client.files.upload(file=iofile, config=types.UploadFileConfig(mime_type="application/pdf"))

            #generating response
            prompt=[upload, "Summarise this file clearly, without any scientific notation or jargon. No extra things to be added, just the summary clearly under 1800 characters."]
            response = await interaction.client.get_cog('GeminiCog').get_gemini_response(prompt)

            # Try to send the summary as a reply to the original user's message
            try:
                    await interaction.channel.send(
                        f"Summary of {self.attachment.filename}:\n\n{response}",
                        reference=discord.MessageReference(message_id=self.msgID, channel_id=interaction.channel.id)
                    )
                    
            except Exception:
                    await interaction.followup.send(f"Summary of {self.attachment.filename}:\n\n{response}")
            try:
                await self.bot_message.delete()
            except:
                pass
            self.stop() #stopping the view so that buttons are not active after one use
        
        except Exception as e:
             if webhookURL:
                webhook.send(f"Error in summarising PDF: \n```{e}```")
             try:
                 await self.bot_message.edit(content=f"Failed to process {self.attachment.filename}", view=None)
             except Exception:                 
                 pass
             self.stop()

    @discord.ui.button(label="Audio Summary", style=discord.ButtonStyle.blurple,emoji="🔊")
    async def audioSummary(self, interaction:discord.Interaction, button:discord.ui.Button):
        #acknowledging the interaction, but defer the response 
        #if this code does not exist, then interaction failed error might occur
        await interaction.response.defer()
        if self.bot_message:
            try:
                await self.bot_message.edit(content=f"Processing {self.attachment.filename}...", view=None)
            except Exception:
                pass
        
        try:
            file_data=await self.attachment.read()
            iofile=io.BytesIO(file_data)
            upload=genAI_client.files.upload(file=iofile, config=types.UploadFileConfig(mime_type="application/pdf"))

            #generating response
            prompt=[upload, "Summarise this file clearly, without any scientific notation or jargon. No extra things to be added, just the summary clearly under 1800 characters."]
            response = await interaction.client.get_cog('GeminiCog').get_gemini_response(prompt)
            try:
                path=f"cogs/TTS/{interaction.guild.id}"
                os.makedirs(path, exist_ok=True)
                outputFilename=f"{self.attachment.filename}_summary.wav"
                fullPath=os.path.join(path, outputFilename)
                
                AZURE_KEY=config.get("azure_speech_key","")
                AZURE_REGION="centralindia"
                
                speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
                audio_config = speechsdk.audio.AudioConfig(filename=fullPath)
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
                synthesizer.speak_text_async(response).get()

                file=discord.File(fullPath)
                try:
                    await interaction.channel.send(
                        content=f"Audio summary of {self.attachment.filename}:",
                        file=file,
                        reference=discord.MessageReference(message_id=self.msgID, channel_id=interaction.channel.id)
                    )
                except Exception as e:
                    await interaction.channel.send(
                        ccontent=f"Audio summary of {self.attachment.filename}:",
                        file=file
                    )

                try:
                    del synthesizer
                except:
                    pass

                for _ in range(5): #retry mechanism to handle file access issues
                    try:
                        os.remove(fullPath)
                        if os.path.exists(path) and not os.listdir(path):
                            os.rmdir(path)
                        break
                    except Exception as e:
                        await asyncio.sleep(1)
                
            except Exception as e:
                if webhookURL:
                    webhook.send(f"Error in generating audio summary: {e}")

            # Try to send the audio summary as a reply to the original user's message
            
            try:
                await self.bot_message.delete()
            except:
                pass
            self.stop() #stopping the view so that buttons are not active after one use
        
        except Exception as e:
             if webhookURL:
                webhook.send(f"Error in summarising PDF: \n```{e}```")
             try:
                 await self.bot_message.edit(content=f"Failed to process {self.attachment.filename}", view=None)
             except Exception:                 
                 pass
             self.stop()
        

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray,emoji="❌")
    async def cancel(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        try:
            await self.bot_message.delete()
        except Exception:
            pass
        self.stop() #stopping the view so that buttons are not active after one use

    
#TEST BUTTON
class testButton(discord.ui.View):
    @discord.ui.button(label="Test", style=discord.ButtonStyle.green)
    async def test(self, interaction:discord.Interaction, button:discord.ui.Button):
        try:
            await interaction.response.send_message("Button works!")
            response="This is a dummy summary for testing the audio summary feature."
            path=f"cogs/TTS/{interaction.guild.id}"
            os.makedirs(path, exist_ok=True)
            outputFilename=f"Test_summary.wav"
            fullPath=os.path.join(path, outputFilename)
            
            AZURE_KEY=config.get("azure_speech_key","")
            AZURE_REGION="centralindia"
            
            speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
            audio_config = speechsdk.audio.AudioConfig(filename=fullPath)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            synthesizer.speak_text_async(response).get()
            
            file=discord.File(fullPath)

            await interaction.channel.send(
                content=f"Test Audio Summary:",
                file=file
            )

            del synthesizer

            for _ in range(5): #retry mechanism to handle file access issues
                try:
                    os.remove(fullPath)
                    if os.path.exists(path) and not os.listdir(path):
                        os.rmdir(path)
                    break
                except:
                    await asyncio.sleep(1)

            if webhookURL:
                webhook.send("Test button was clicked!")
        except Exception as e:
          try:
            os.remove(fullPath)
            if os.path.exists(path) and not os.listdir(path):
                os.rmdir(path)
          except:
            pass
        

  
class fileLogic(commands.Cog):
    def __init__(self, client):
        self.client = client
        if webhookURL:
            webhook.send("fileLogic.py loaded")
    

    #test command for buttons
    @commands.command()
    async def testpdf(self, ctx):
        await ctx.send("This is a test message", view=testButton())
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.lower().endswith('.pdf'):
                    view=pdfButtons(attachment, msgID=message.id)
                    msg=await message.reply(content=f"What do you want to do with {attachment.filename}?", view=view)
                    # attach the sent bot message to the view so it can be edited later
                    try:
                        view.set_bot_message(msg)
                    except Exception:
                        pass

                    break

async def setup(client):
    await client.add_cog(fileLogic(client))





